import pygame
import numpy as np
from threading import RLock
from abc import abstractmethod, ABCMeta
from game.update import Update

class AbstractMiniGame(ABCMeta):
    def __init__(self, screen: pygame.Surface):
        self.screen       = screen
    
    @abstractmethod
    def apply_update(self, update: Update):
        pass

    @abstractmethod
    def get_pixels(self) -> np.ndarray:
        pass
