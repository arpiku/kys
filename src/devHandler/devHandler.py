import re
import sys
import select
import atexit
import termios
from evdev import ecodes as e, list_devices, AbsInfo, InputDevice, categorize

class devHandler():
    def __init__(self,ev_handler,device_dir="/dev/input"):
        self.ev_handler = ev_handler

    def get_devices(self):
        devices = [InputDevice(path) for path in list_devices()]

    def event_generator(self):
        fd_to_device = {dev.fd: dev for dev in devices}
        while True:
            r, w, e = select.select(fd_to_device, [], [])
            for fd in r:
                for event in fd_to_device[fd].read():
                    yield(event)

 


         
