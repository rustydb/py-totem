import time

import board

from neopixel import NeoPixel
     
from analogio import AnalogIn
PIXELS_PIN = board.A1
PIXELS_NUM = 71
RED = (255, 0, 0)
ORANGE = (255, 20, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

onboard = NeoPixel(board.NEOPIXEL, 1)
onboard.brightness = 0.1
pixels = NeoPixel(PIXELS_PIN, PIXELS_NUM, brightness=0.1)
vbat_voltage = AnalogIn(board.D9)


def color_chase(color: tuple, wait: float) -> None:
    """
    Lights each LED to the given color one at a time.
    :param color: RGB color tuple to chase with.
    :param wait: Time before lighting next LED.
    """
    for i in range(PIXELS_NUM):
        pixels[i] = color
        time.sleep(wait)


def set_voltage_led() -> None:
    """
    Sets the LED to a color corresponding to roughly: "full charge",
    "good charge", "fair charge", and "low".
    """
    battery_voltage = (vbat_voltage.value * 3.3) / 65536 * 2
    if battery_voltage >= 3.7:
        onboard.fill(GREEN)
    elif 3.5 <= battery_voltage < 3.7:
        onboard.fill(YELLOW)
    elif 3.3 <= battery_voltage < 3.5:
        onboard.fill(ORANGE)
    elif battery_voltage < 3.3:
        onboard.fill(RED)
    else:
        onboard.fill(CYAN)
    onboard.show()


def rainbow_cycle() -> None:
    """
    Makes a rainbow over PIXELS_NUM.
    """
    for i in range(PIXELS_NUM):

        # LED position * number of colors floor divided by number of pixels plus current color.
        rc_index = (i * 256 // PIXELS_NUM) + 1

        # Set pixel RGB tuple set by wheel()
        pixels[i] = wheel(rc_index & 255)


def wheel(pos: int) -> tuple:
    """
    Converts an integer from 0 - 255 to an RGB color value. The colors are a transition
    r - g - b - back to r.
    :param pos: Position on the color wheel (0 - 255).
    :returns: RGB Tuple.
    """
    # If out of range, return black.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return 255 - pos * 3, pos * 3, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3
    pos -= 170
    return pos * 3, 0, 255 - pos * 3


# Main run loop.
while True:

    # Red is the "cheapest visible" color for "power-on" LED.
    set_voltage_led()
    for color in [RED, YELLOW, GREEN, CYAN, BLUE, PURPLE]:
        set_voltage_led()
        color_chase(color, 0.01)
        set_voltage_led()
        rainbow_cycle()
