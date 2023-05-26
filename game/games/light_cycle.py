import pygame
import numpy as np

from collections import deque
from game.mini_game import AbstractMiniGame 
from game.update import UPDATE_UP, UPDATE_DOWN, UPDATE_LEFT, UPDATE_RIGHT
from pygame.math import Vector2

PLAYER_INDICES = [1, 2]

# Fixme
PLAYER_START_POSITIONS = [
    None,
    (0,  0), # player 1
    (20, 20), # player 2
]
PLAYER_COLORS = [
    None,
    (255, 255,   0), # player 1
    (  0, 255, 255), # player 2
]

# Milliseconds between light-cycle movement
TIME_STEP = 100

# Milliseconds to buffer input
INPUT_BUFFER_TIME = TIME_STEP * 2

class LightCycleGame(AbstractMiniGame):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()
        
        self.restart_game()
        
    def update_screen(self):
        self.screen.fill((0, 0, 0))

        # Draw players
        for player_index in PLAYER_INDICES:
            for pos in self.player_queues[player_index]:
                pygame.draw.line(self.screen, PLAYER_COLORS[player_index], pos, pos, 1)

    def apply_update(self, update=None):
        # Push update onto queue if an update was supplied
        if update != None:
            current_time = pygame.time.get_ticks()
            self.player_queues[update.player_index].appendleft((update.button, current_time))

        # Move based on fixed time steps
        self.time_accumulator += self.clock.get_time()

        # TODO(zack): Figure out this time accumulator stuff
        # while self.time_accumulator >= TIME_STEP:
        for player_index in PLAYER_INDICES:
            # Ignore dead players
            if self.player_queues[player_index] == None:
                continue
            self.move_player(player_index)

        # Detect win condition
        if sum(x is not None for x in self.player_queues) == 1:
            print(f"LightCycle: someone has won.")
            self.restart_game()
            return


    def move_player(self, player_index):
        current_time = pygame.time.get_ticks()
        prev_direction = self.curr_directions[player_index]
        next_direction = prev_direction

        # Get subsequent valid move directions, until a different one is found
        while len(self.move_queues[player_index]) > 0:
            (potential_next_direction, input_time) = self.move_queues[player_index].pop()
            if current_time < input_time + INPUT_BUFFER_TIME:
                next_direction = potential_next_direction
                if next_direction != prev_direction:
                    break

        # Find next head position
        next_head_pos = self.get_next_head_pos(player_index, next_direction)
        
        # Apply next head position
        self.player_queues[player_index].appendleft(next_head_pos)

        # Detect death condition
        did_hit_wall = self.check_hit_wall(player_index)
        did_hit_someone = self.check_hit_anyone(player_index)

        if did_hit_wall or did_hit_someone:
            print(f"Light Cycle: player {player_index} is dead.")
            self.kill_player(player_index)
            return

    def get_next_head_pos(self, player_index, next_direction):
        (x, y) = self.player_queues[player_index][0]
        curr_direction = self.curr_directions[player_index]
        head_copy = Vector2(x, y)

        # Set curr_direction if valid next_direction is given
        changing_direction_from_vert = \
          (curr_direction == UPDATE_UP or curr_direction == UPDATE_DOWN) and \
            (next_direction == UPDATE_LEFT or next_direction == UPDATE_RIGHT)
        changing_direction_from_horz = \
          (curr_direction == UPDATE_LEFT or curr_direction == UPDATE_RIGHT) and \
            (next_direction == UPDATE_UP or next_direction == UPDATE_DOWN)
        if changing_direction_from_vert or changing_direction_from_horz:
            self.curr_directions[player_index] = next_direction

        # Get next head position
        if curr_direction == UPDATE_UP:
            head_copy.y -= 1
        elif curr_direction == UPDATE_DOWN:
            head_copy.y += 1
        elif curr_direction == UPDATE_LEFT:
            head_copy.x -= 1
        elif curr_direction == UPDATE_RIGHT:
            head_copy.x += 1

        return head_copy

    def check_hit_wall(self, player_index):
        head = self.player_queues[player_index][0]
        return (head.x < 0 or head.x >= self.width or
                head.y < 0 or head.y >= self.height)
    
    def check_hit_anyone(self, player_index):
        head = self.player_queues[player_index][0]

        # For each player...
        for other_player_index in PLAYER_INDICES:
            other_iter_player_queue = iter(self.player_queues[other_player_index])

            # Skip head if self
            if player_index == other_player_index:
                next(other_iter_player_queue)

            # Check for collision between head and other player bits
            for pos in other_iter_player_queue:
                if pos == head:
                    return True

        return False

    def kill_player(self, player_index):
        self.player_queues[player_index] = None

    def restart_game(self):
        print("restarting running")
        self.time_accumulator = 0
        self.move_queues = [
            None,
            deque(), # player 1
            deque(), # player 2
        ]
        self.player_queues: list[deque] = [
            None,
            deque([Vector2(PLAYER_START_POSITIONS[1][0], PLAYER_START_POSITIONS[1][1])]), # player 1
            deque([Vector2(PLAYER_START_POSITIONS[2][0], PLAYER_START_POSITIONS[2][1])]), # player 2
        ]
        self.curr_directions = [
            None,
            UPDATE_RIGHT, # player 1
            UPDATE_LEFT,  # player 2
        ]
