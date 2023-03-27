from config.config import config

strip = None

def get_strip():
    global strip
    
    if strip is not None:
        return strip
    
    if config.get('is_dev'):
        from leds.dev import GUIPixelStrip 
        strip = GUIPixelStrip(None, None, None, None)
    else:
        from leds.prod import get_prod_strip
        strip = get_prod_strip()
    
    strip.begin()
    return strip

def get_color():
    if config.get('is_dev'):
        from leds.dev import GUIColor 
        return GUIColor
    else:
        from rpi_ws281x import Color
        return Color
