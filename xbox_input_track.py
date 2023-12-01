import evdev

def find_xbox_controller():
    # Iterate over input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    # Look for Xbox controller in device names
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path
    
    return None

# Replace '/dev/input/event2' with the correct event device path
event_device_path = find_xbox_controller()

try:
    xbox_series_controller = evdev.InputDevice(event_device_path)
    print(f"Xbox Series controller found: {xbox_series_controller.name}")

    # Read input events
    for event in xbox_series_controller.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                print(f"X-axis event at {event.timestamp()}, {evdev.ecodes.ABS[event.code]}: {event.value}")
            elif event.code == evdev.ecodes.ABS_Z:
                print(f"Left trigger event at {event.timestamp()}, {evdev.ecodes.ABS[event.code]}: {event.value}")
            elif event.code == evdev.ecodes.ABS_RZ:
                print(f"Right trigger event at {event.timestamp()}, {evdev.ecodes.ABS[event.code]}: {event.value}")

except FileNotFoundError:
    print(f"Error: Could not find the specified event device at {event_device_path}")
except PermissionError:
    print(f"Error: Permission denied. Try running the script with elevated privileges using 'sudo'.")
except Exception as e:
    print(f"Error: {e}")
