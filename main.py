from leds.strip import get_strip
from game.driver import CitArcadeGameDriver
from time import sleep
from leds.visualizer import Visualizer
from calibration.calibrator import Calibrator
import numpy as np

if __name__ == "__main__":

    side_length = 9
    horz_panels = 4
    vert_panels = 4
    num_pixels = side_length ** 2 * horz_panels * vert_panels

    strip = get_strip()
    strip.begin()

    c = Calibrator(9, 4, 4)
    def illuminate_pixel(i):
        strip.setPixelColorRGB(i, 1, 0, 0)

    c.do_tty_calibration(illuminate_pixel)

    game_driver = CitArcadeGameDriver(36, 36)
    visualizer = Visualizer(side_length, horz_panels, vert_panels)

    # Actual painting
    arr = game_driver.paint(0, 0).reshape((num_pixels, 3)) / 255
    print(arr)
    input("Press [enter] to show first set of random colors.")
    visualizer.displayColors(arr)

    input("Press [enter] to exit.")