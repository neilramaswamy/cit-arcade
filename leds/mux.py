from config.config import config

# In this file, we multiplex the production and development strip/Color interfaces onto the one
# needed by the application. Imports statements are guarded because the rpi_ws281x library is not
# available on MacOS (in development), and it's unnecessary for us to install dev dependencies (like
# Matplotlib on the actual rpi).

if config.get('is_dev'):
    from leds.dev import GUIColor 
    Color = GUIColor
else:
    from rpi_ws281x import Color as RpiColor
    Color = RpiColor


strip = None

if config.get('is_dev'):
    from leds.dev import get_dev_strip 
    strip = get_dev_strip()
else:
    from leds.prod import get_prod_strip
    strip = get_prod_strip()

strip.begin()