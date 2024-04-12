import argparse
import evdev
import os
import re

import types
import importlib.util #To bind the functions in the generated file

from selectors import DefaultSelector, EVENT_READ #To allow selecting multiple devices


chosen_devices = {}
devices_dict = {}


def importCode(code, module_name):

    module = types.ModuleType(module_name)
    exec(code, module.__dict__)

    return module

def bind_key_macros(choices,filename):
    #grab the devices
    #Bind the functions in the config file to the keystrokesS
    code = ""
    with open(f"{filename}/{filename}.py","r") as fp:

        code = fp.read()

    m = importCode(code,f"{filename}")
    m.func_KEY_Q_16()

    selector = DefaultSelector()
    for choice in choices:
        devices_dict[choice].grab()
        selector.register(devices_dict[choice],EVENT_READ)
    while True:
        for key,mask in selector.select():
            device = key.fileobj
            for event in device.read():
                print(evdev.categorize(event))
                print(type(event))
                print(event.code)
                print(evdev.ecodes.KEY[event.code])
                print(event.type)
                print(event.value)

                print(f"m.func_{evdev.ecodes.KEY[event.code]}_{event.code}()")
                exec(f"m.func_{evdev.ecodes.KEY[event.code]}_{event.code}()")

    

def create_config(name,keys):
    name = name.replace(' ', '_')
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    try:
        os.mkdir(f"{name}")
    except:
        print("File Already There")
    try:
        open(f"{name}/__init__.py", "a").close()
    except:
        print("__init__ file already there")
    
    for key in keys:
        if isinstance(key[0],list):
            continue
        with open(f"{name}/{name}.py","a+") as fp:
            fp.write(f"def func_{key[0]}_{key[1]}():\n\tpass\n")

    return name
        
    

def create_dev_dict():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for i,dev in enumerate(devices):
        devices_dict[i] = dev


def list_devices():
    dev_format = "{0:<3} {1.path:<20} {1.name:<35} {1.phys:<35} {1.uniq:<4}"
    for index,device in devices_dict.items():
        print(dev_format.format(index,device))

def create_map(choices):
    filename = "none"
    print(devices_dict)
    macro_dict = {}
    for choice in choices:
        dev_input_dict = devices_dict[int(choice)].capabilities(verbose=True)
        for key in dev_input_dict:
            if key[0] == 'EV_KEY':
                macro_dict[devices_dict[int(choice)].name] = dev_input_dict[key]

    for name,keys in macro_dict.items():
        filename = create_config(name,keys)
        print(f"{name}.py created successfully!")

    return filename






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
    filename = "none"

    if confirmation.lower() in ["y", "yes"] and choices.issubset(set(devices_dict.keys())):
        filename = create_map(choices)
    elif confirmation.lower() in ["n", "no"]:
        print("Exiting...")
    else:
        print("Invalid Input Try Again")

    confirmation = input(f"Start the macros?  confirm (y/n): ")

    if confirmation.lower() in ["y", "yes"]:
        print(filename)
        bind_key_macros(choices,filename)

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

