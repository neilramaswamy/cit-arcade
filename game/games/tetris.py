import pygame
import numpy as np

from collections import deque
from game.games.tetris_pieces import NUM_SHAPES, SHAPE_COLORS, TetrisPiece
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2
from random import randint

# Milliseconds between dropping
TIME_STEP = 500

class TetrisGame(AbstractMiniGame):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()
        
        self.restart_game()
        
    def update_screen(self):
        self.screen.fill((0, 0, 0))

        # Draw grid
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                pos = self.grid_top_left + Vector2(x, y)
                shape_index = self.grid[x][y]
                if shape_index == -1:
                    continue
                pygame.draw.line(self.screen, SHAPE_COLORS[shape_index], pos, pos, 1)
        
        # Draw active piece
        for pos in self.piece.get_positions():
            if not (pos[0] < 0 or pos[0] >= self.grid_width or
                    pos[1] < 0 or pos[1] >= self.grid_height):
                pygame.draw.line(self.screen, SHAPE_COLORS[self.piece.shape_index], pos, pos, 1)

    def apply_update(self, update=None):
        # If an update is provided, try to move
        if update != None:
            self.piece_move(update.button)

        # Do not auto-fall if less than some time
        self.time_accumulator += self.clock.get_time()
        if self.time_accumulator < TIME_STEP:
            return
        else:
            self.time_accumulator -= TIME_STEP

        # Auto-fall
        self.piece.y += 1
        if self.piece_in_valid_space():
            return
        
        # Cannot fall; must lock. Also detect loss condition
        self.piece.y -= 1
        for pos in self.piece.get_positions():
            if pos[1] < 0:
                print(f"Tetris: you are dead.")
                self.restart_game()
                return
            self.grid[tuple(pos)] = self.piece.shape_index

        # Check for completed rows
        self.clear_completed_rows()
        
        # Generate next piece
        self.piece = self.get_new_piece()

    def piece_move(self, direction):
        if   direction == UPDATE_UP:
            self.piece.rotation += 1
            if not self.piece_in_valid_space():
                self.piece.rotation -= 1
        elif direction == UPDATE_DOWN:
            self.piece.y += 1
            if not self.piece_in_valid_space():
                self.piece.y -= 1
        elif direction == UPDATE_LEFT:
            self.piece.x -= 1
            if not self.piece_in_valid_space():
                self.piece.x += 1
        elif direction == UPDATE_RIGHT:
            self.piece.x += 1
            if not self.piece_in_valid_space():
                self.piece.x -= 1
        else:
            print("Tetris: invalid direction.")
            
    def piece_in_valid_space(self) -> bool:
        for pos in self.piece.get_positions():
            if pos[0] < 0 or pos[0] >= self.grid_width:
                return False
            elif pos[1] >= self.grid_height:
                return False
            elif pos[1] < 0:
                continue
            elif self.grid[tuple(pos)] != -1:
                return False
        return True
    
    def get_new_piece(self) -> TetrisPiece:
        return TetrisPiece(self.grid_width // 2, 0, randint(0, NUM_SHAPES - 1))
    
    def clear_completed_rows(self):
        cleared = np.all(self.grid != -1, axis=0)
        num_cleared = np.sum(cleared)

        indices = np.arange(self.grid_height)
        indices[cleared] = -1
        indices = np.sort(indices)[num_cleared:]

        self.grid[:, num_cleared:] = self.grid[:, indices]
        self.grid[:, :num_cleared] = -1

    def restart_game(self):
        self.time_accumulator = 0
        self.grid_top_left = Vector2((0,0)) # Should be ... something
        self.grid_height = self.height      # Should be 20, usually
        self.grid_width  = self.width       # Should be 10, usually
        self.grid = np.full((self.grid_width, self.grid_height), -1) # Contains shape indices
        self.piece = self.get_new_piece()
