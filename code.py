import time

import board

import neopixel

PIXELS_PIN = board.A1
PIXELS_NUM = 72
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

onboard = neopixel.NeoPixel(board.NEOPIXEL, 1)
onboard.brightness = 0.1
pixels = neopixel.NeoPixel(PIXELS_PIN, PIXELS_NUM, brightness=0.7, auto_write=False)


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


def color_chase(color: tuple, wait: float) -> None:
    """
    Lights each LED to the given color one at a time.
    :param color: RGB color tuple to chase with.
    :param wait: Time before lighting next LED.
    """

    # Loop through each pixel.
    for i in range(PIXELS_NUM):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()

    # Wait before any other function call so full strand can be lit.
    time.sleep(0.5)


def rainbow_cycle(wait: float) -> None:
    """
    Makes a rainbow over PIXELS_NUM.
    :param wait: The time to cycle for the rainbow.
    """

    # Loop through each color (0 - 255).
    for j in range(255):

        # Loop through each LED.
        for i in range(PIXELS_NUM):

            # LED position * number of colors floor divided by number of pixels plus current color.
            rc_index = (i * 256 // PIXELS_NUM) + j

            # Set pixel RGB tuple set by wheel()
            pixels[i] = wheel(rc_index & 255)

        # Light up the LEDs and wait until next color.
        pixels.show()
        time.sleep(wait)


# Main run loop.
while True:
    onboard.fill(GREEN)
    onboard.show()
    color_chase(PURPLE, 0.1)
    onboard.fill(RED)
    onboard.show()
    color_chase(BLUE, 0.1)
    onboard.fill(BLUE)
    onboard.show()
    rainbow_cycle(0.1)
