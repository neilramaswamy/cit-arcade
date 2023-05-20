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

# get_strip looks a bit clunky with these arguments but this is somewhat intentional.
#
# In production, the physical dimensions of the display are fixed. The underlying strip instance
# doesn't need to know anything about itself. But in development, the strip is actually a wrapper
# around some PyPlot, and to draw the plot, it needs to know its dimensions. Thus, these arguments
# here are used only by the development strip to know how much to draw.
#
# One question is, then: why not just hard-code dimensions into the dev strip so that it looks and
# quacks like a production strip? In development, we generally want to try lots of different
# dimensions, so it's useful to be able to dynamically pass this to the strip.
def get_strip(horz_side_length, vert_side_length, horz_panels, vert_panels):
    global strip

    if strip is not None:
        return strip

    if config.get('is_dev'):
        from leds.dev import get_dev_strip 
        strip = get_dev_strip(horz_side_length, vert_side_length, horz_panels, vert_panels)
    else:
        if (horz_side_length or vert_side_length or horz_panels or vert_panels):
            print("WARNING: In production, strip dimensions are fixed. Ignoring passed in dimensions.")

        from leds.prod import get_prod_strip
        strip = get_prod_strip(horz_side_length * horz_panels, vert_side_length * vert_panels)

    strip.begin()
    return strip