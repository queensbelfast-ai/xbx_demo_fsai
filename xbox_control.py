import evdev
import curses

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

# Function to normalize values to the range -1.0 to 1.0
def normalize_value(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 2 - 1

def main(stdscr):
    xbox_series_controller = evdev.InputDevice(event_device_path)
    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch() non-blocking

    while True:
        event = xbox_series_controller.read_one()
        if event and event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                normalized_x = normalize_value(event.value, -32768, 32767)
                stdscr.addstr(0, 0, f"X-axis: {normalized_x}")
            elif event.code == evdev.ecodes.ABS_Z:
                normalized_trigger = normalize_value(event.value, 0, 1023)
                stdscr.addstr(1, 0, f"Left trigger: {normalized_trigger}")
            elif event.code == evdev.ecodes.ABS_RZ:
                normalized_trigger = normalize_value(event.value, 0, 1023)
                stdscr.addstr(2, 0, f"Right trigger: {normalized_trigger}")

            stdscr.refresh()

def run_curses():
    curses.wrapper(main)

if __name__ == "__main__":
    run_curses()
