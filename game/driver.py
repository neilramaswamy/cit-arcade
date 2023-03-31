import os
from threading import RLock, Thread
from typing import List, Optional

import numpy as np
import pygame

from game.mini_game import AbstractMiniGame
from game.renderer import render_to_strip
from game.update import UPDATE_SELECT, UPDATE_START, Update
from leds.mux import get_strip
from mapper.map import ensure_panel_config
from webserve.webserve import do_webserve
from game.games.snake import SnakeGame

# When set to "dummy", the PyGame window will not appear
os.environ["SDL_VIDEODRIVER"] = "dummy"

class CitArcadeGameDriver():
    def __init__(self, height: int, width: int, updates: list, updates_lock: RLock):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.clock = pygame.time.Clock()

        self.updates: List[Update] = updates
        self.updates_lock: RLock = updates_lock

        self.paused: bool = False
        self.active_game: Optional[AbstractMiniGame] = SnakeGame(self.screen, self.clock)
    
    def apply_updates(self):
        self.updates_lock.acquire()

        while len(self.updates) > 0:
            update = self.updates.pop(0)

            # Select/Start commands are always handled by the top-level game; other updates can be
            # dispatched to the underlying active game if there is one
            if update.type == UPDATE_SELECT:
                if self.active_game:
                    self.paused = True
            elif update.type == UPDATE_START:
                # If there is a game that is selected, play the game
                self.handle_start()
            elif self.active_game:
                self.active_game.apply_update(update)
            else:
                print(f"Discarding update {update}")
        
        self.updates_lock.release()

        if self.active_game:
            self.active_game.apply_update(None)
    
    def get_pixels(self):
        if self.active_game:
            if self.paused:
                # Render the paused screen
                pass
            else:
                return self.active_game.get_pixels()
        else:
            # Render the main menu
            pass
    
    def render_main_menu(self):
        pass

    def render_paused_screen(self):
        pass


if __name__ == "__main__":
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
    game = CitArcadeGameDriver(vert_pixels, horz_pixels, updates, updates_lock)


    # Run event thread in background
    event_thread.start()
    print("got here?")

    while True:
        game.apply_updates()
        pixels = game.get_pixels()

        render_to_strip(strip, pixels, panel_config.mapping)
        game.clock.tick(30)