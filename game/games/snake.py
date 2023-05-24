import pygame
import numpy as np

from collections import deque
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2
from random import randint

# Fixme
START_POS = (5, 5)

FOOD_COLOR = (255, 0, 0)
SNAKE_COLOR = (255, 255, 255)

# Milliseconds between snake movement
TIME_STEP = 200

# Milliseconds to buffer input
INPUT_BUFFER_TIME = TIME_STEP * 1.5

class SnakeGame(AbstractMiniGame):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()
        
        self.restart_game()
        
    def update_screen(self):
        self.screen.fill((0, 0, 0))

        # Draw food
        pygame.draw.line(self.screen, FOOD_COLOR, self.food_pos, self.food_pos, 1)

        # Draw snake
        for pos in self.snake_queue:
            pygame.draw.line(self.screen, SNAKE_COLOR, pos, pos, 1)

    def apply_update(self, update=None):
        # Push update onto queue if an update was supplied
        if update != None:
            self.move_queue.appendleft((update.button, pygame.time.get_ticks()))

        # Do nothing if less than some time
        self.time_accumulator += self.clock.get_time()
        if self.time_accumulator < TIME_STEP:
            return
        else:
            self.time_accumulator -= TIME_STEP

        # Pop off queue to get next valid move, if any
        next_direction = None
        while next_direction == None and len(self.move_queue) > 0:
            (potential_next_direction, input_time) = self.move_queue.pop()
            if pygame.time.get_ticks() < input_time + INPUT_BUFFER_TIME:
                next_direction = potential_next_direction

        if next_direction == None:
            next_direction = self.curr_direction
            
        self.move(next_direction)

    def move(self, next_direction):
        # Find next head position
        next_head_pos = self.get_next_head_pos(next_direction)
        
        # Apply next head position
        self.snake_queue.appendleft(next_head_pos)

        # Detect food collision
        if next_head_pos == self.food_pos:
            self.food_pos = self.get_new_food_pos()
        else: 
            self.snake_queue.pop()

        # Detect win condition
        if len(self.snake_queue) == self.height * self.width:
            print(f"Snake: you have won.")
            self.restart_game()
            return

        # Detect lose condition
        if self.check_hit_wall() or self.check_hit_self():
            print(f"Snake: you are dead.")
            self.restart_game()
            return

    def get_next_head_pos(self, next_direction):
        (x, y) = self.snake_queue[0]
        head_copy = Vector2(x, y)

        # Set self.curr_direction if valid next_direction is given
        changing_direction_from_vert = \
          (self.curr_direction == UPDATE_UP or self.curr_direction == UPDATE_DOWN) and \
            (next_direction == UPDATE_LEFT or next_direction == UPDATE_RIGHT)
        changing_direction_from_horz = \
          (self.curr_direction == UPDATE_LEFT or self.curr_direction == UPDATE_RIGHT) and \
            (next_direction == UPDATE_UP or next_direction == UPDATE_DOWN)
        if changing_direction_from_vert or changing_direction_from_horz:
            self.curr_direction = next_direction

        # Get next head position
        if   self.curr_direction == UPDATE_UP:
            head_copy.y -= 1
        elif self.curr_direction == UPDATE_DOWN:
            head_copy.y += 1
        elif self.curr_direction == UPDATE_LEFT:
            head_copy.x -= 1
        elif self.curr_direction == UPDATE_RIGHT:
            head_copy.x += 1

        return head_copy

    def check_hit_wall(self):
        head = self.snake_queue[0]
        return (head.x < 0 or head.x >= self.width or
                head.y < 0 or head.y >= self.height)
    
    def check_hit_self(self):
        head = self.snake_queue[0]
        iter_snake_queue = iter(self.snake_queue)
        next(iter_snake_queue) # skip head
        for pos in iter_snake_queue:
            if pos == head:
                return True
        return False

    def get_new_food_pos(self):
        new_food_pos = Vector2()
        invalid = True

        # Try to get a valid food position
        while invalid:
            new_food_pos = Vector2((randint(0, self.width - 1),
                                    randint(0, self.height - 1)))
            invalid = False
            for pos in self.snake_queue:
                if pos == new_food_pos:
                    invalid = True
                    
        return new_food_pos

    def restart_game(self):
        self.time_accumulator = 0
        self.move_queue = deque()
        self.snake_queue = deque([ # Fixme?
            Vector2(START_POS),
            Vector2(START_POS) - Vector2((1,0)),
            Vector2(START_POS) - Vector2((2,0))
        ])
        self.food_pos = self.get_new_food_pos()
        self.curr_direction = UPDATE_RIGHT
