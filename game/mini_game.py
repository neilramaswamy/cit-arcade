from abc import ABCMeta, abstractmethod
from threading import RLock
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
        If update is None, then we're asking the game to do a tick.

        If update is not None, there is user input that the game might consider applying to its
        internal state.
        """
        pass

    @abstractmethod
    def get_pixels(self) -> np.ndarray:
        pass
