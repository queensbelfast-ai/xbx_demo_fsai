import Jetson.GPIO as GPIO
import time

# Define the GPIO pins connected to the LEDs
led_pins = [11, 13, 15, 16, 18, 22, 29, 31, 32, 33]

def setup_leds():
    GPIO.setmode(GPIO.BOARD)
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def test_leds():
    try:
        while True:
            for pin in led_pins:
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(0.5)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        setup_leds()
        test_leds()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()
