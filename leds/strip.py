from config.config import IS_DEV
from leds.dev import GUIPixelStrip

def get_strip():
    if IS_DEV:
        return GUIPixelStrip
    else:
        # Linux something something
        return None