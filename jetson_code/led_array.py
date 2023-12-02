import time
import Jetson.GPIO as GPIO
import evdev

def find_xbox_controller():
    # Iterate over input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    # Look for Xbox controller in device names
    for device in devices:
        if "Generic X-Box pad" in device.name:
            return device.path
    
    return None

# Define the LED pins for Jetson Nano J41 GPIO header
led_pins = [11, 13, 15, 16, 18, 22, 29, 31, 32, 33]

# Number of LEDs
num_leds = len(led_pins)

# Initialize LED pins as outputs
GPIO.setmode(GPIO.BOARD)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)

# Find Xbox Series controller
event_device_path = find_xbox_controller()

try:
    xbox_series_controller = evdev.InputDevice(event_device_path)
    print(f"Xbox Series controller found: {xbox_series_controller.name}")

    # Read input events
    for event in xbox_series_controller.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_RZ:
                rt_val = event.value
                rt_leds = int((rt_val / 1023.0) * num_leds / 2)
                rt_leds = max(0, min(rt_leds, num_leds // 2))

                for i, pin in enumerate(led_pins[:num_leds // 2]):
                    GPIO.output(pin, GPIO.HIGH if i < rt_leds else GPIO.LOW)

            elif event.code == evdev.ecodes.ABS_Z:
                lt_val = event.value
                lt_leds = int((lt_val / 1023.0) * num_leds / 2)
                lt_leds = max(0, min(lt_leds, num_leds // 2))

                for i, pin in enumerate(led_pins[num_leds // 2:]):
                    GPIO.output(pin, GPIO.HIGH if i < lt_leds else GPIO.LOW)

except FileNotFoundError:
    print(f"Error: Could not find the specified event device at {event_device_path}")
except PermissionError:
    print(f"Error: Permission denied. Try running the script with elevated privileges using 'sudo'.")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up GPIO
    GPIO.cleanup()
