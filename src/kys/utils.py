import re
import sys
import select
import atexit
import termios
from evdev import ecodes as e, list_devices, AbsInfo, InputDevice, categorize



def output_events(devices):
    print("Listening for events (press ctrl-c to exit) ...")
    fd_to_device = {dev.fd: dev for dev in devices}
    while True:
        r, w, e = select.select(fd_to_device, [], [])
        for fd in r:
            for event in fd_to_device[fd].read():
                print_event(event)

    

def device_test(grab_devices=False, print_capabilities_of_dev=False):
    devices = select_devices()

    if grab_devices:
        for dev in devices:
            dev.grab()

    if print_capabilities_of_dev:
        for dev in devices:
            print_capabilities(dev)

    if not devices:
        devices = [InputDevice(path) for path in devices]


    # Disable tty echoing if stdin is a tty.
    if sys.stdin.isatty():
        toggle_tty_echo(sys.stdin, enable=False)
        atexit.register(toggle_tty_echo, sys.stdin, enable=True)

    output_events(devices)



def select_devices(device_dir="/dev/input"):
    """
    Select one or more devices from a list of accessible input devices.
    """

    def devicenum(device_path):
        digits = re.findall(r"\d+$", device_path)
        return [int(i) for i in digits]

    devices = sorted(list_devices(device_dir), key=devicenum)
    devices = [InputDevice(path) for path in devices]
    if not devices:
        msg = "error: no input devices found (do you have rw permission on %s/*?)"
        print(msg % device_dir, file=sys.stderr)
        sys.exit(1)

    dev_format = "{0:<3} {1.path:<20} {1.name:<35} {1.phys:<35} {1.uniq:<25}"
    dev_lines = [dev_format.format(num, dev) for num, dev in enumerate(devices)]

    print("ID  {:<20} {:<35} {:<35} {}".format("Device", "Name", "Phys", "Uniq"))
    print("-" * len(max(dev_lines, key=len)))
    print("\n".join(dev_lines))
    print()

    choices = input("Select devices [0-%s]: " % (len(dev_lines) - 1))

    try:
        choices = choices.split()
        choices = [devices[int(num)] for num in choices]
    except ValueError:
        choices = None

    if not choices:
        msg = "error: invalid input - please enter one or more numbers separated by spaces"
        print(msg, file=sys.stderr)
        sys.exit(1)

    return choices


def print_capabilities(device):
    capabilities = device.capabilities(verbose=True)
    input_props = device.input_props(verbose=True)

    print("Device name: {.name}".format(device))
    print("Device info: {.info}".format(device))
    # print("Repeat settings: {}\n".format(device.repeat))

    if ("EV_LED", ecodes.EV_LED) in capabilities:
        leds = ",".join(i[0] for i in device.leds(True))
        print("Active LEDs: %s" % leds)

    active_keys = ",".join(k[0] for k in device.active_keys(True))
    print("Active keys: %s\n" % active_keys)

    if input_props:
        print("Input properties:")
        for type, code in input_props:
            print("  %s %s" % (type, code))
        print()

    print("Device capabilities:")
    for type, codes in capabilities.items():
        print("  Type {} {}:".format(*type))
        for code in codes:
            # code <- ('BTN_RIGHT', 273) or (['BTN_LEFT', 'BTN_MOUSE'], 272)
            if isinstance(code[1], AbsInfo):
                print("    Code {:<4} {}:".format(*code[0]))
                print("      {}".format(code[1]))
            else:
                # Multiple names may resolve to one value.
                s = ", ".join(code[0]) if isinstance(code[0], list) else code[0]
                print("    Code {:<4} {}".format(s, code[1]))
        print("")


def print_event(e):
    print(categorize(e))
    if e.type == ecodes.EV_SYN:
        if e.code == ecodes.SYN_MT_REPORT:
            msg = "time {:<16} +++++++++ {} ++++++++"
        else:
            msg = "time {:<16} --------- {} --------"
        print(msg.format(e.timestamp(), ecodes.SYN[e.code]))
    else:
        if e.type in ecodes.bytype:
            codename = ecodes.bytype[e.type][e.code]
        else:
            codename = "?"

        evfmt = "time {:<16} type {} ({}), code {:<4} ({}), value {}"
        print(evfmt.format(e.timestamp(), e.type, ecodes.EV[e.type], e.code, codename, e.value))


def get_devices_with_id(ids = None):
    if not ids:
        print("id Missing")
        return None
    devices = [InputDevice(path) for path in list_devices() if InputDevice(path).uniq in ids]
    return devices

def toggle_tty_echo(fh, enable=True):
    flags = termios.tcgetattr(fh.fileno())
    if enable:
        flags[3] |= termios.ECHO
    else:
        flags[3] &= ~termios.ECHO
    termios.tcsetattr(fh.fileno(), termios.TCSANOW, flags)


if __name__ == "__main__":
    try:
        ret = device_test()
    except (KeyboardInterrupt, EOFError):
        ret = 0
    sys.exit(ret)
