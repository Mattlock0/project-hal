from gpiozero import RGBLED, MotionSensor
from time import sleep
import enum


class Color(enum.Enum):
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (1, 0, 0)
    YELLOW = (1, 0.5, 0)
    PURPLE = (1, 0, 1)
    CYAN = (0, 1, 1)
    WHITE = (1, 1, 1)
    OFF = (0, 0, 0)


class ColorID(enum.IntEnum):
    RED = 1
    GREEN = 2
    BLUE = 3


# GPIO pins
LED_RED_PIN = 1
LED_GREEN_PIN = 7
LED_BLUE_PIN = 8
MOTION_SENSOR_PIN = 4

MOTION_SENSOR_DELAY = 0  # in seconds


class MSLED:
    def __init__(self, ms_enabled=True) -> None:
        self.led = RGBLED(red=LED_RED_PIN, green=LED_GREEN_PIN, blue=LED_BLUE_PIN, pwm=True)
        self.sensor = MotionSensor(MOTION_SENSOR_PIN)
        # leds.pulse()

        self.ms_enabled = ms_enabled

        if self.ms_enabled:
            # setting up watchers
            self.sensor.when_motion = lambda x: self.keep_on()
            self.sensor.when_no_motion = self.led.off

    def set_color(self, red: float, green: float, blue: float):
        if red < 0 or red > 1:
            print(f'Value of {red} invalid value for color. Resetting to 0.')
            red = 0
        if green < 0 or green > 1:
            print(f'Value of {green} invalid value for color. Resetting to 0.')
            green = 0
        if blue < 0 or blue > 1:
            print(f'Value of {blue} invalid value for color. Resetting to 0.')
            blue = 0

        self.led.color = (red, green, blue)

    def manual_color_input(self):
        red = float(input('Enter the value for red LED: '))
        green = float(input('Enter the value for green LED: '))
        blue = float(input('Enter the value for blue LED: '))

        self.set_color(red, green, blue)

    def keep_on(self):
        self.led.on()
        sleep(MOTION_SENSOR_DELAY)

    def fade_in_color(self, color: ColorID):
        # fading in the chosen LED
        # find a better way to do this, like with a dict or pointer
        for n in range(100):
            if color == ColorID.RED:
                self.led.red = n / 100
            elif color == ColorID.GREEN:
                self.led.green = n / 100
            elif color == ColorID.BLUE:
                self.led.blue = n / 100
            sleep(0.1)
