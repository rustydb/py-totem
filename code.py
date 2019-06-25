import time

import board

from neopixel import NeoPixel
import random
from analogio import AnalogIn

# Data leads.
CORE_PIN = board.A1
ORB_PIN = board.A2

# LED no.
CORE_NUM = 71
ORB_NUM = 4

# Color definitions.
RED = (255, 0, 0)
ORANGE = (255, 20, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

# Initialize all devices.
onboard = NeoPixel(board.NEOPIXEL, 1)
onboard.brightness = 0.1
core_pixels = NeoPixel(CORE_PIN, CORE_NUM, brightness=0.6)
orb_pixels = NeoPixel(ORB_PIN, ORB_NUM, brightness=0.8)
vbat_voltage = AnalogIn(board.D9)


def color_chase(color: tuple, wait: float) -> None:
    """
    Lights each LED to the given color one at a time.
    :param color: RGB color tuple to chase with.
    :param wait: Time before lighting next LED.
    """
    for i in reversed(range(CORE_NUM)):
        core_pixels[i] = color
        for j in range(ORB_NUM):
            orb_pixels[j] = color
        time.sleep(wait)


def set_voltage_led() -> None:
    """
    Sets the LED to a color corresponding to roughly: "full charge",
    "good charge", "fair charge", and "low".
    """
    battery_voltage = (vbat_voltage.value * 3.3) / 65536 * 2
    if battery_voltage >= 3.7:
        onboard.fill(GREEN)
    elif 3.5 < battery_voltage < 3.7:
        onboard.fill(YELLOW)
    elif 3.3 < battery_voltage < 3.5:
        onboard.fill(ORANGE)
    elif battery_voltage < 3.3:
        onboard.fill(RED)
    else:
        # TODO: Come back here and make this better.
        onboard.fill(CYAN)
    onboard.show()


def rainbow_cycle(start_index: int = 0) -> None:
    """
    Makes a rainbows.
    """
    for i in range(CORE_NUM):

        # LED position * number of colors floor divided by number of core_pixels plus current color.
        rc_index = (i * 256 // CORE_NUM * 2) + 1 & 255

        # Set pixel RGB tuple set by wheel().
        if i + start_index >= CORE_NUM:
            core_pixels[abs(i - start_index)] = wheel(rc_index)
        else:
            core_pixels[i + start_index] = wheel(rc_index)
        for j in range(ORB_NUM):
            orb_pixels[j] = wheel(rc_index)
    if start_index >= CORE_NUM:
        return 0
    return start_index
    # rainbow_cycle(start_index)
    # color_chase(wheel(rc_index), 0.01)    


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
    start_index = 0
    for color in [PURPLE, CYAN, BLUE, GREEN]:
        set_voltage_led()
        color_chase(color, 0.01)
        set_voltage_led()
        start_index = rainbow_cycle(start_index)
        start_index = start_index + 2
