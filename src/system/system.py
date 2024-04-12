import evdev


def get_system():
    return evdev


def input_devices(system):
    return [system.InputDevice(path) for path in system.list_devices()]



if __name__ == "__main__":
    init = get_system()
    print(input_devices(init)[5])


    
