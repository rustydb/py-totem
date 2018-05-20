import time
import board
import neopixel

PIXELS_PIN = board.A1
PIXELS_NUM = 1
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

onboard = neopixel.NeoPixel(board.NEOPIXEL, 1)
onboard.brightness = 1.0
pixels = neopixel.NeoPixel(PIXELS_PIN, PIXELS_NUM, brightness=0.3, auto_write=False)


def wheel(pos: int) -> tuple:
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return 255 - pos * 3, pos * 3, 0
    if pos < 170:
        pos -= 85
        return 0, 255 - pos * 3, pos * 3
    pos -= 170
    return pos * 3, 0, 255 - pos * 3


def color_chase(color: int, wait: float) -> None:
    for i in range(PIXELS_NUM):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait: float) -> None:
    for j in range(255):
        for i in range(PIXELS_NUM):
            rc_index = (i * 256 // PIXELS_NUM) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    onboard.fill(PURPLE)
    onboard.show()
    time.sleep(1)
    onboard.fill(CYAN)
    onboard.show()
    time.sleep(1)
    onboard.fill(RED)
    onboard.show()
    time.sleep(1)
