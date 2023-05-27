import pygame
import numpy as np

from collections import deque
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2
from random import randint

class GradGame(AbstractMiniGame):
    def __init__(self, screen: pygame.SurfaceType, clock):
        self.screen = screen
        self.clock  = clock

        self.font = pygame.font.SysFont("munrosmall", 10)

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()

        self.congrats = self.font.render("Congrats", False, (255, 0, 0))
        self.class_num = self.font.render("2023!", False, (255, 0, 0))
        
    def update_screen(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.congrats, (0, 0))

        class_num_offset = (self.congrats.get_width() - self.class_num.get_width()) // 2
        self.screen.blit(self.class_num, (class_num_offset, 10))

    def apply_update(self, update=None):
        return