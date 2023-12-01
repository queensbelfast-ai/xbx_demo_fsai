import evdev

def find_xbox_controller():
    # Iterate over input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    # Look for Xbox controller in device names
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path
    
    return None

print(find_xbox_controller())
