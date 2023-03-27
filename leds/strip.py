from leds.dev import GUIPixelStrip
from leds.prod import get_prod_strip
from rpi_ws281x import PixelStrip, Color

IS_DEV = True 

def get_strip():
    if IS_DEV:
        return GUIPixelStrip(None, None, None, None)
    else:
        return get_prod_strip()