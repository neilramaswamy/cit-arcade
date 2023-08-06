import os
from threading import RLock, Thread
from typing import Callable, List, Optional

from game.manager import CitArcadeGameManager
from game.renderer import render_to_strip
from game.update import UPDATE_PAUSE, UPDATE_SELECT, Update, UPDATE_UP, UPDATE_DOWN
from leds.mux import get_strip
from mapper.map import ensure_panel_config
from webserve.webserve import do_webserve

"""
This project can run in two modes:

1. Python mode, which already has a web server for user-interaction, games, and GIF rendering
2. Interop mode, which exposes primitives to easily paint pixels to the screen from any language

Python mode is the default, and it is what you get when you run `python driver.py`.

Two primitive functions are exposed for interop mode, which are:

    1. initialize-screen, which returns a tuple of the form [num_rows, num_columns]
    2. paint-screen, which takes a 3D matrix of the form [num_rows, num_columns, 3] of RGB pixels

Users using interop mode will have to implement any more complicated features themselves.
"""

class InteropModeDriver():
    def __init__(self):
        self.strip = None
        self.panel_config = None

    def initialize_screen(self):
        # Do the calibration
        self.panel_config = ensure_panel_config()

        horz_side_length = self.panel_config.horz_side_length
        vert_side_length = self.panel_config.vert_side_length
        horz_panels = self.panel_config.horz_panels
        vert_panels = self.panel_config.vert_panels

        print(f"Initialized the screen and strip")
        self.strip = get_strip(horz_side_length, vert_side_length, horz_panels, vert_panels)

        vert_pixels = vert_panels * vert_side_length
        horz_pixels = horz_panels * horz_side_length

        # Return the number of rows and columns
        return (vert_pixels, horz_pixels)

    def paint_screen(self, pixels):
        # TODO: Validate the dimensions of matrix
        render_to_strip(self.strip, pixels, self.panel_config.mapping)


class PythonModeDriver():
    def __init__(self):
        panel_config = ensure_panel_config()
        print(panel_config)

        horz_side_length = panel_config.horz_side_length
        vert_side_length = panel_config.vert_side_length
        horz_panels = panel_config.horz_panels
        vert_panels = panel_config.vert_panels

        strip = get_strip(horz_side_length, vert_side_length, horz_panels, vert_panels)

        vert_pixels = vert_panels * vert_side_length
        horz_pixels = horz_panels * horz_side_length

        updates = []
        updates_lock = RLock()

        event_thread = Thread(name="webserve", target=do_webserve, args=(updates, updates_lock))
        game = CitArcadeGameManager(vert_pixels, horz_pixels, updates, updates_lock)

        # Run event thread in background
        event_thread.start()

        while True:
            game.apply_updates()
            pixels = game.get_pixels()

            render_to_strip(strip, pixels, panel_config.mapping)

            # If the game is paused and the clock keeps going, then the underlying arcade games
            # will think they're in the future when they're resumed. A quick fix is to not tick that
            # clock when the game is paused.
            #
            # But if the game driver needs a clock to render its own animations, we'd want to keep
            # that going. In that case, we might consider including TWO clocks—one for the game driver
            # (which never stops), and one for the actual mini-games.
            if not game.paused:
                game.clock.tick(30)

if __name__ == "__main__":
    PythonModeDriver()