class PixelStrip(object):
    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False,
            brightness=255, channel=0, strip_type=None, gamma=None):
        """Class to represent a SK6812/WS281x LED display.  Num should be the
        number of pixels in the display, and pin should be the GPIO pin connected
        to the display signal line (must be a PWM pin like 18!).  Optional
        parameters are freq, the frequency of the display signal in hertz (default
        800khz), dma, the DMA channel to use (default 10), invert, a boolean
        specifying if the signal line should be inverted (default False), and
        channel, the PWM channel to use (defaults to 0).
        """
        pass

    def will_not_implement(self):
        raise Exception("Will not implement!")

    def begin(self):
        """Initialize library, must be called once before other functions are
        called.
        """
        # TODO
        pass

    def show(self):
        """Update the display with the data from the LED buffer."""
        pass

    def setPixelColor(self, n, color):
        """Set LED at position n to the provided 24-bit color value (in RGB order).
        """
        pass

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        """Set LED at position n to the provided red, green, and blue color.
        Each color component should be a value from 0 to 255 (where 0 is the
        lowest intensity and 255 is the highest intensity).
        """
        pass

    def setGamma(self, gamma):
        self.will_not_implement()

    def getBrightness(self):
        self.will_not_implement()

    def setBrightness(self, brightness):
        """Scale each LED in the buffer by the provided brightness.  A brightness
        of 0 is the darkest and 255 is the brightest.
        """
        self.will_not_implement()

    def getPixels(self):
        """Return an object which allows access to the LED display data as if
        it were a sequence of 24-bit RGB values.
        """
        self.will_not_implement()

    def numPixels(self):
        """Return the number of pixels in the display."""
        self.will_not_implement()

    def getPixelColor(self, n):
        """Get the 24-bit RGB color value for the LED at position n."""
        self.will_not_implement()

    def getPixelColorRGB(self, n):
        self.will_not_implement()
    
    def getPixelColorRGBW(self, n):
        self.will_not_implement()
