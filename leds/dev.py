import numpy as np
import matplotlib.pyplot as plt
from leds.visualizer import Visualizer

def GUIColor(red, green, blue, white=0):
    """Convert the provided red, green, blue color to a 24-bit color value.
    Each color component should be a value 0-255 where 0 is the lowest intensity
    and 255 is the highest intensity.
    """
    return [red, green, blue]

class GUIPixelStrip(object):

    def __init__(self, display_conf, one_to_two_map, num,
            pin, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0,
            strip_type=None, gamma=None):
        """Class to represent a SK6812/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 10), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """

        self.ready = False

        self.side_length = 10 # display_conf.panel_side_length
        self.horz_panels = 1 # display_conf.num_horizontal_panels
        self.vert_panels = 1 # display_conf.num_vertical_panels

        self.visualizer = Visualizer(
            self.side_length, 
            self.horz_panels, 
            self.vert_panels)
        
        self.num_pixels = self.side_length ** 2 * self.horz_panels * self.vert_panels
        self.colors = np.zeros((self.num_pixels, 3))

    def will_not_implement(self):
        raise Exception("Will not implement!")

    def begin(self):
        self.ready = True
        print("LED strip ready")

    def show(self):
        """
        Update the display with the data from the LED buffer.
        """

        if not self.ready: raise Exception("Must call begin()")

        self.visualizer.displayColors(self.colors)

    def setPixelColor(self, n, color):
        if not self.ready: raise Exception("Must call begin()")

        self.colors[n] = np.array(color) / 255

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        """
        Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        
        if not self.ready: raise Exception("Must call begin()")

        self.colors[n] = np.array([red, green, blue]) / 255

    def setGamma(self, _):
        self.will_not_implement()

    def getBrightness(self):
        self.will_not_implement()

    def setBrightness(self, _):
        self.will_not_implement()

    def getPixels(self):
        self.will_not_implement()

    def numPixels(self):
        return self.num_pixels

    def getPixelColor(self, _):
        self.will_not_implement()

    def getPixelColorRGB(self, _):
        self.will_not_implement()
    
    def getPixelColorRGBW(self, _):
        self.will_not_implement()

if __name__ == "__main__":
    
    strip = GUIPixelStrip(0,0,0,0)

    strip.begin()

    for i in range(150):
        input("Press [enter] to set next pixel.")
        strip.setPixelColorRGB(i, 255, 255, 255)
        strip.show()

    input("Press [enter] to finish.")