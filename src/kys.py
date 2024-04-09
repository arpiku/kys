import argparse
import evdev
import os
import re


chosen_devices = {}
devices_dict = {}


def create_config(name,):
    name = name.replace(' ', '_')
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    with open(f"name.py","w")
    

def create_dev_dict():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for i,dev in enumerate(devices):
        devices_dict[i] = dev


def list_devices():
    dev_format = "{0:<3} {1.path:<20} {1.name:<35} {1.phys:<35} {1.uniq:<4}"
    for index,device in devices_dict.items():
        print(dev_format.format(index,device))

def create_map(choices):
    print(devices_dict)
    macro_dict = {}
    for choice in choices:
        dev_input_dict = devices_dict[int(choice)].capabilities(verbose=True)
        for key in dev_input_dict:
            if key[0] == 'EV_KEY':
                macro_dict[devices_dict[int(choice)].name] = dev_input_dict[key]

    for name,keys in macro_dict.items():
        create_config(name,keys)






def choose_devices():
    list_devices()
    num_devices = len(devices_dict)
    choices = input(f"Select devices [0-{num_devices}] seperated with spaces: ")
    choices = choices.split()
    try:
        choices = [int(num) for num in choices ]
    except ValueError:
        print('Invalid input. Please enter integers separated by spaces.')

    confirmation = input(f"Your Selections are {choices} confirm (y/n): ")
    choices = set(choices)

    if confirmation.lower() in ["y", "yes"] and choices.issubset(set(devices_dict.keys())):
        create_map(choices)
    elif confirmation.lower() in ["n", "no"]:
        print("Exiting...")
    else:
        print("Invalid Input Try Again")


        
def main():
    create_dev_dict()
    kys = argparse.ArgumentParser(prog='kys',
                                  description='''A command line tool to convert you keyboards into macro boards!''',
                                  epilog='''vesion = ''')

    kys.add_argument("command", metavar = "cmd", help="Choose from [list, init, start, stop]")

    kys.add_argument("-c","--choose",dest="chosen_list",action="extend", nargs="+", type=int)
    kys.add_argument("-e","--explain",dest="explain_list",action="extend", nargs="+", type=int)

    args = kys.parse_args()

    if(args.command == "list"):
        list_devices()
    if(args.command == "choose"):
        choose_devices()



if __name__ == "__main__":
    main()

