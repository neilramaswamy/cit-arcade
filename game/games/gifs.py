import pygame
import numpy as np

from collections import deque
import os
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2
from random import randint

FRAME_RATE = 24
FRAME_DELAY = (1000) / FRAME_RATE

class GifGame(AbstractMiniGame):
    def __init__(self, screen: pygame.SurfaceType, clock):
        self.screen = screen
        self.clock  = clock

        self.font = pygame.font.SysFont("munrosmall", 10)

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()

        self.should_rerender = True

        self.frames: list[pygame.SurfaceType] = []
        for (_, _, filenames) in os.walk("game/assets/sonic"):
            ordered_filenames = sorted(filenames)

            for filename in ordered_filenames:
                img = pygame.image.load(os.path.join("game/assets/sonic", filename))
                img = pygame.transform.scale(img, (36, 40))

                self.frames.append(img)
        
        self.index = 0
        
    def update_screen(self):
        self.screen.fill((0, 0, 0)) 
        self.screen.blit(self.frames[self.index], (0, 0))

        self.index = (self.index + 1) % len(self.frames)

        pygame.display.update()

    def apply_update(self, update=None):
        return