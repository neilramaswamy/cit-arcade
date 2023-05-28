import pygame
import numpy as np

from collections import deque
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2
from random import randint

class FaceGame(AbstractMiniGame):
    def __init__(self, screen: pygame.SurfaceType, clock):
        self.screen = screen
        self.clock  = clock

        self.font = pygame.font.SysFont("munrosmall", 10)

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()

        self.should_rerender = True

        self.image = pygame.image.load("game/assets/rachel.png")
        self.image = pygame.transform.scale(self.image, (36, 40))
        
    def update_screen(self):
        if not self.should_rerender:
            return
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.image, (0, 0))

        pygame.display.update()
        self.should_rerender = False

    def apply_update(self, update=None):
        return