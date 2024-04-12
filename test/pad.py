import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
   print(device.path, device.name, device.phys)


dev = evdev.InputDevice('/dev/input/event21')
dev.grab()

for event in dev.read_loop():
   print(evdev.categorize(event))
