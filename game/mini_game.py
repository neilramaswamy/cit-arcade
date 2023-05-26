from abc import ABCMeta, abstractmethod
from typing import Optional

import numpy as np
import pygame

from game.update import Update


class AbstractMiniGame():
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock  = clock
    
    @abstractmethod
    def apply_update(self, update: Optional[Update]):
        """
        If update is None, then we're asking the game to do a tick, i.e. move the snake in Snake
        one pixel forward.

        If update is not None, there is user input that the game should apply to its
        internal state.

        An Update has a field called "button", which can be up/down/left/right, or enter.
        """
        pass

    @abstractmethod
    def update_screen(self):
        """
        Every clock tick, this function is called. It should update self.screen.
        """
        pass
