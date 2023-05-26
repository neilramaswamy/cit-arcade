import pygame
import numpy as np

from typing import Optional
from game.update import Update

from game.mini_game import AbstractMiniGame

class ConwaysGameOfLife(AbstractMiniGame):
    col_about_to_die = (200, 200, 225)
    col_alive = (255, 255, 215)
    col_background = (10, 10, 40)
    col_grid = (30, 30, 60)
    sz = 8

    def __init__(self, screen: pygame.SurfaceType, clock):
        self.screen = screen
        self.clock = clock

        self.height = 40
        self.width  = 36

        self.cells = np.zeros((self.height, self.width))
        pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
        pos = (3,3)
        self.cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern

    # We shouldn't receive any updates for this
    def apply_update(self, update: Optional[Update]):
        return

    def update_screen(self):
        print("updating screen for conway")
        nxt = np.zeros((self.cells.shape[0], self.cells.shape[1]))

        for r, c in np.ndindex(self.cells.shape):
            num_alive = np.sum(self.cells[r-1:r+2, c-1:c+2]) - self.cells[r, c]

            if self.cells[r, c] == 1 and num_alive < 2 or num_alive > 3:
                col = self.col_about_to_die
            elif (self.cells[r, c] == 1 and 2 <= num_alive <= 3) or (self.cells[r, c] == 0 and num_alive == 3):
                nxt[r, c] = 1
                col = self.col_alive

            col = col if self.cells[r, c] == 1 else self.col_background
            pygame.draw.rect(self.screen, col, (c*self.sz, r*self.sz, self.sz-1, self.sz-1))

        self.cells = nxt