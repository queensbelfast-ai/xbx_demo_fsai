import evdev

def find_xbox_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path
    
    return None

stick = 0 
lt_val = 0
rt_val = 0

# Replace '/dev/input/event2' with the correct event device path
event_device_path = find_xbox_controller()

try:
    xbox_series_controller = evdev.InputDevice(event_device_path)
    print(f"Xbox Series controller found: {xbox_series_controller.name}")

    # Initialize previous values
    prev_stick = None
    prev_lt_val = None
    prev_rt_val = None

    # Read input events
    for event in xbox_series_controller.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                # Check if Y-axis value is less than -400
                y_value = xbox_series_controller.absinfo(evdev.ecodes.ABS_Y).value
                if y_value < -400:
                    # Map X-axis value to an angle (if needed)
                    stick = int((event.value / 32767.0) * 90)
                    if stick != prev_stick:
                        print(f"Left Stick X: {stick}")
                        prev_stick = stick
            elif event.code == evdev.ecodes.ABS_Z:
                lt_val = event.value
                if lt_val != prev_lt_val:
                    print(f"Left Trigger: {lt_val}")
                    prev_lt_val = lt_val
            elif event.code == evdev.ecodes.ABS_RZ:
                rt_val = event.value
                if rt_val != prev_rt_val:
                    print(f"Right Trigger: {rt_val}")
                    prev_rt_val = rt_val

except FileNotFoundError:
    print(f"Error: Could not find the specified event device at {event_device_path}")
except PermissionError:
    print(f"Error: Permission denied. Try running the script with elevated privileges using 'sudo'.")
except Exception as e:
    print(f"Error: {e}")
