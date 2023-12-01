import evdev
import curses

# Replace '/dev/input/event6' with the correct event device path
event_device_path = '/dev/input/event6'

# Function to normalize values to the range -1.0 to 1.0
def normalize_value(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 2 - 1

def draw_slider(stdscr, y, value, label, color_pair):
    slider_width = 60
    slider_fill = int((value + 1) * slider_width / 2)
    slider_display = f"[{'#' * slider_fill}{' ' * (slider_width - slider_fill)}]"

    stdscr.addstr(y * 2, 0, f"{label}: {slider_display} {value:.5f}", curses.color_pair(1) | curses.A_BOLD)

    for i in range(slider_width):
        if i < slider_fill:
            stdscr.chgat(y * 2, i + len(label) + 3, 1, curses.color_pair(color_pair) | curses.A_BOLD)

def setup_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

def main(stdscr):
    xbox_series_controller = evdev.InputDevice(event_device_path)
    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch() non-blocking
    setup_colors()

    # Set the title
    title = "Queen's AI Formula Student Demo"
    stdscr.addstr(0, (curses.COLS - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)

    while True:
        event = xbox_series_controller.read_one()
        if event and event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                normalized_x = normalize_value(event.value, -32768, 32767)
                draw_slider(stdscr, 1, normalized_x, "Steering Angle", 1)
            elif event.code == evdev.ecodes.ABS_Z:
                normalized_left_trigger = normalize_value(event.value, 0, 1023)
                draw_slider(stdscr, 2, normalized_left_trigger, "Left Pedal    ", 2)
            elif event.code == evdev.ecodes.ABS_RZ:
                normalized_right_trigger = normalize_value(event.value, 0, 1023)
                draw_slider(stdscr, 3, normalized_right_trigger, "Right Pedal   ", 3)

            stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
