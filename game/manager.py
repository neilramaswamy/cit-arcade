import os
from threading import RLock 
from typing import Callable, List, Optional

import numpy as np
import pygame

from game.games.snake import SnakeGame
from game.games.tetris import TetrisGame
from game.games.light_cycle import LightCycleGame
from game.games.face import FaceGame
from game.games.gifs import GifGame
from game.games.conway import ConwaysGameOfLife
from game.mini_game import AbstractMiniGame
from game.games.grad import GradGame
from game.update import UPDATE_PAUSE, UPDATE_SELECT, Update, UPDATE_UP, UPDATE_DOWN

# When set to "dummy", the PyGame window will not appear
os.environ["SDL_VIDEODRIVER"] = "dummy"

# TODO: Ideally we should generate this based on the size of the screen
# Do you really think I have time for this?
MAX_HOME_MENU_OPTIONS = 4

class MenuOption():
    def __init__(self, name: str, on_click: Callable[[None], None]):
        self.name = name
        self.click = on_click 

class CitArcadeGameManager():
    def __init__(self, height: int, width: int, updates: list, updates_lock: RLock):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.clock = pygame.time.Clock()

        self.updates: List[Update] = updates
        self.updates_lock: RLock = updates_lock

        self.paused: bool = False
        self.active_game: Optional[AbstractMiniGame] = None

        self.home_options: List[MenuOption] = [
            MenuOption("Gifs", self._set_active_game(GifGame)),
            MenuOption("Face", self._set_active_game(FaceGame)),
            MenuOption("Snake", self._set_active_game(SnakeGame)),
            MenuOption("Tetris", self._set_active_game(TetrisGame)),
            MenuOption("Grad", self._set_active_game(GradGame)),
            MenuOption("Tron", self._set_active_game(LightCycleGame)),
            MenuOption("Conway", self._set_active_game(ConwaysGameOfLife))
        ]
        self.paused_options: List[MenuOption] = [
            MenuOption("Resume", self._return_to_game),
            MenuOption("Exit", self._return_to_home)
        ]

        # Load the font up-front since that seems to take time
        self.font = pygame.font.SysFont("munrosmall", 10)

        # If the game is paused, then it indexes into self.paused_options
        # If the game is not paused, it indexes into self.home_options
        self.option_index = 0

    def _set_active_game(self, Game: AbstractMiniGame):
        def F():
            self.active_game = Game(self.screen, self.clock)

        return F
    
    def _return_to_game(self):
        self.paused = False
        self.option_index = 0

    def _return_to_home(self):
        self.paused = False
        self.active_game = None
        self.option_index = 0
    
    def _go_to_paused(self):
        self.paused = True
        self.option_index = 0
    
    def apply_updates(self):
        self.updates_lock.acquire()

        # TODO: Suppose update[0] is pause, update[1] is down, and update[2] is start. This is a bit
        # of an edge case, but this could end up with the game being cancelled unintentionally,
        # because the update[1] was made THINKING it would be applied to the real game, not the
        # menu.
        #
        # One option is to completely flush the updates buffer once we receive a mode change, or
        # we could think of a more sophisticated way to apply update to the game state.
        while len(self.updates) > 0:
            update = self.updates.pop(0)

            is_pause_screen = self.active_game != None and self.paused
            is_game_screen = self.active_game != None and not self.paused
            is_home_screen = self.active_game == None

            if is_home_screen:
                self._handle_menu_move(update, self.home_options)
            elif is_pause_screen:
                self._handle_menu_move(update, self.paused_options)
            elif is_game_screen:
                if update.button == UPDATE_PAUSE:
                    self._go_to_paused()
                else:
                    self.active_game.apply_update(update)
            else:
                raise Exception("Invalid state")

        self.updates_lock.release()

        if self.active_game:
            self.active_game.apply_update(None)

    def _handle_menu_move(self, update: Update, options: List[MenuOption]) -> bool:
        if update.button == UPDATE_UP:
            self.option_index = max(self.option_index - 1, 0)
            return True
        elif update.button == UPDATE_DOWN:
            self.option_index = min(self.option_index + 1, len(options) - 1)
            return True
        elif update.button == UPDATE_SELECT:
            options[self.option_index].click()
            return True
        return False
    
    def get_pixels(self):
        if self.active_game:
            if self.paused:
                self.render_paused_screen()
            else:
                self.active_game.update_screen()
        else:
            self.render_home_menu()
        
        arr = pygame.surfarray.array3d(self.screen)
        return np.transpose(arr, axes=(1, 0, 2))
    
    def render_home_menu(self):
        self.screen.fill((0, 0, 0))

        # We only render MAX_HOME_MENU_OPTIONS at a time, so we have to figure out what window
        # of elements to show. We start the four items in front of the current position,
        # self.option_index, unless we're near the end.
        start_menu_index = max(0, self.option_index - (MAX_HOME_MENU_OPTIONS - 1))
        curr_home_options = self.home_options[start_menu_index:start_menu_index+MAX_HOME_MENU_OPTIONS]

        for i, option in enumerate(curr_home_options):
            option_index = i + start_menu_index

            selected_str = "»" if option_index == self.option_index else " "
            img = self.font.render(f"{selected_str}{option.name}", False, (255, 0, 0))
            self.screen.blit(img, (0, i * 10 - 2))

    def render_paused_screen(self):
        self.screen.fill((0, 0, 0))

        for i, option in enumerate(self.paused_options):
            selected_str = "»" if i == self.option_index else " "
            img = self.font.render(f"{selected_str}{option.name}", False, (255, 0, 0))
            self.screen.blit(img, (0, i * 10 - 2))
