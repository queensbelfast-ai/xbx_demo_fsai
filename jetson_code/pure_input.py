import evdev

def find_xbox_controller():
    # Iterate over input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    # Look for Xbox controller in device names
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path
    
    return None

stick = 0 
lt_val = 0
rt_val =0 

# Replace '/dev/input/event2' with the correct event device path
event_device_path = find_xbox_controller()

try:
    xbox_series_controller = evdev.InputDevice(event_device_path)
    print(f"Xbox Series controller found: {xbox_series_controller.name}")

    # Read input events
    for event in xbox_series_controller.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                stick = event.value
                print(stick)
            elif event.code == evdev.ecodes.ABS_Z:
                lt_val = event.value
                print(lt_val)
            elif event.code == evdev.ecodes.ABS_RZ:
                rt_val = event.value
                print(rt_val)

except FileNotFoundError:
    print(f"Error: Could not find the specified event device at {event_device_path}")
except PermissionError:
    print(f"Error: Permission denied. Try running the script with elevated privileges using 'sudo'.")
except Exception as e:
    print(f"Error: {e}")
