from config.config import IS_DEV
from leds.dev import GUIPixelStrip
from calibration.schemas import SchemaDisplayConf

def get_strip():
    if IS_DEV:
        return GUIPixelStrip(None, None, None, None)
    else:
        raise Exception("LEDStrip not implemented for production yet")