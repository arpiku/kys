from evdev import InputDevice, ecodes, UInput

ABS_X = ecodes.ABS_X
ABS_Y = ecodes.ABS_Y
ABS_TILT_X = ecodes.ABS_TILT_X
ABS_TILT_Y = ecodes.ABS_TILT_Y

device_path = '/dev/input/event21'  # Replace X with the event number of your device

device = InputDevice(device_path)

ui = UInput()

def map_to_mouse(value, min_value, max_value, min_mouse, max_mouse):
    return int(((value - min_value) / (max_value - min_value)) * (max_mouse - min_mouse) + min_mouse)

for event in device.read_loop():
    print(event.type)
    print(event.code)
    print(event.value)
    mouse_x = 0
    mouse_y = 0
    if event.type == ecodes.EV_ABS:
        if event.code == ABS_X:
            # Map ABS_X value to mouse X coordinate (adjust min/max values as needed)
            mouse_x = map_to_mouse(event.value, 0, 32767, 0, 1920)  # Example mapping
        elif event.code == ABS_Y:
            # Map ABS_Y value to mouse Y coordinate (adjust min/max values as needed)
            mouse_y = map_to_mouse(event.value, 0, 32767, 0, 1080)  # Example mapping
        elif event.code == ABS_TILT_X:
            # Handle ABS_TILT_X for additional functionality if needed
            pass
        elif event.code == ABS_TILT_Y:
            # Handle ABS_TILT_Y for additional functionality if needed
            pass

        # Emit mouse movement events to the virtual input device
        ui.write(ecodes.EV_REL, ecodes.REL_X, mouse_x)
        ui.write(ecodes.EV_REL, ecodes.REL_Y, mouse_y)
        ui.syn()
