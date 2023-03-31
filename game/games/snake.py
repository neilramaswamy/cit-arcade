import pygame
import numpy as np

from collections import deque
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2
from random import randint

START_POS = (5, 5)

SNAKE_COLOR = (255, 255, 255)

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class SnakeGame(AbstractMiniGame):
    def __init__(self, screen, updates: list):
        self.screen  = screen
        self.updates = updates

        self.height = 40 # fixme
        self.width  = 36 # fixme

        self.snake_queue = deque([Vector2(START_POS)])

    def get_pixels(self):
        self.screen.fill((0, 0, 0))

        # Draw food
        pygame.draw.circle(self.screen, SNAKE_COLOR, pos, 1)

        # Draw snake
        for pos in self.snake_queue:
            pygame.draw.circle(self.screen, SNAKE_COLOR, pos, 1)

        arr = pygame.surfarray.array3d(self.screen)
        return np.transpose(arr, axes=(1, 0, 2))

    def apply_update(self, update):
        # Find next head position
        head_copy = self.snake_queue[0].copy
        if   update.type == UPDATE_UP:
            head_copy.y -= 1
        elif update.type == UPDATE_DOWN:
            head_copy.y += 1
        elif update.type == UPDATE_LEFT:
            head_copy.x -= 1
        elif update.type == UPDATE_RIGHT:
            head_copy.x += 1
        else:
            return
        
        # Apply next head position
        self.snake_queue.appendleft(head_copy)

        # Detect win condition
        if len(self.snake_queue) == self.height * self.width:
            print(f"Snake: you have won. There is nothing more I can teach you, young grasshopper.")
            return # fixme

        # Detect lose condition
        if self.check_hit_wall() or self.check_hit_self():
            print(f"Snake: you are dead.")
            return # fixme
        
        # Detect food collision
        if head_copy == self.food_pos:
            self.spawn_new_food()
        else: 
            self.snake_queue.pop()

    def check_hit_wall(self):
        head = self.snake_queue[0]
        return (head.x < 0 or head.x >= self.width or
                head.y < 0 or head.y >= self.height)
    
    def check_hit_self(self):
        head = self.snake_queue[0]
        for pos in self.snake_queue:
            if pos == head:
                return True
        return False

    def spawn_new_food(self):
        new_food_pos = Vector2()
        invalid = True

        # Try to get a valid food position
        while invalid:
            new_food_pos = Vector2((randint(0, self.width),
                                    randint(0, self.height)))
            invalid = False
            for pos in self.snake_queue:
                if pos == new_food_pos:
                    invalid = True
            
        self.food_pos = new_food_pos
            
        
            

       
        

