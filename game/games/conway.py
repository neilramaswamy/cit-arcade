import pygame
import numpy as np
import time

from typing import Optional
from game.update import Update

from game.mini_game import AbstractMiniGame

class ConwaysGameOfLife(AbstractMiniGame):
    color_alive = (255, 255, 215)
    color_background = (10, 10, 40)

    board = np.array([])

    sz = 1
    generation_time = 0.5
    generation = 0

    def __init__(self, screen: pygame.SurfaceType, clock):
        self.screen = screen
        self.clock = clock
        self.height = 40
        self.width  = 36

        self.board = self.create_initial_board(self.height, self.width)

    def create_initial_board(self, rows: int, cols: int) -> np.ndarray:
        # Create a random board
        # 0 = dead cell, 1 = alive cell
        return np.random.randint(0, 2, size=(rows, cols), dtype=int)

    # We shouldn't receive any updates for this
    def apply_update(self, update: Optional[Update]):
        return

    def update_screen(self):
        print(f"Updating generation {self.generation}")
        self.board = self.get_next_generation(self.board)

        for r, c in np.ndindex(self.board.shape):
            color = self.color_alive if self.board[r, c] else self.color_background
            pygame.draw.rect(self.screen, color, (c*self.sz, r*self.sz, self.sz, self.sz))

        time.sleep(self.generation_time)
        self.generation += 1

    def get_next_generation(self, board: np.ndarray) -> np.ndarray:
        # This is a brute-force implementation of Conway's Game of Life
        # It is not optimized for performance
        # would probably use a moving window with a convolve operation to make it faster. but takes 10ms per gen
        rows, cols = board.shape
        next_board = np.zeros((rows, cols), dtype=int)
        start = time.time()
        for r in range(rows):
            for c in range(cols):
                live_neighbors = sum(
                    board[nr][nc]
                    for nr in range(max(0, r-1), min(rows, r+2))
                    for nc in range(max(0, c-1), min(cols, c+2))
                    if (nr, nc) != (r, c)
                )
                if board[r][c] == 1 and live_neighbors in (2, 3):
                    next_board[r][c] = 1
                elif board[r][c] == 0 and live_neighbors == 3:
                    next_board[r][c] = 1
        print(f'Took {time.time() - start}')
        return next_board