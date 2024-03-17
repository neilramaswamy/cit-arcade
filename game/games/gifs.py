import os

import pygame

from game.mini_game import AbstractMiniGame
from game.update import UPDATE_LEFT, UPDATE_RIGHT

FRAME_RATE = 24
FRAME_DELAY = (1000) / FRAME_RATE

class GifGame(AbstractMiniGame):
    def __init__(self, screen: pygame.SurfaceType, clock):
        self.screen = screen
        self.clock  = clock

        self.font = pygame.font.SysFont("munrosmall", 10)

        # The index into self.gifs, which gives the current gif
        self.gif_index = 0
        # The frame within the current gif that we're going to play
        self.frame_index = 0
        # The number of full iterations we've done so far for the current gif
        self.loops_for_curr_gif = 0

        self.gifs = ["congrats", "blueno", "nyancat", "fire", "stars"]

        self.height = self.screen.get_height()
        self.width  = self.screen.get_width()

        self.frames: list[list[pygame.SurfaceType]] = [[] for _ in range(len(self.gifs))]

        for i, gif in enumerate(self.gifs):
            base_path = f"game/assets/{gif}"

            for (_, _, filenames) in os.walk(base_path):
                ordered_filenames = sorted(filenames)

                for filename in ordered_filenames:
                    file_path = os.path.join(base_path, filename)
                    img = pygame.image.load(file_path)
                    img = pygame.transform.scale(img, (self.width, self.height))

                    self.frames[i].append(img)

    def update_screen(self):
        self.screen.fill((0, 0, 0)) 
        self.screen.blit(self.frames[self.gif_index][self.frame_index], (0, 0))

        # Loop back to the start of the gif. We advance the gif with the
        # user-specified Updates in apply_update.
        if (self.frame_index == len(self.frames[self.gif_index]) - 1):
            self.frame_index = 0
        else:
            self.frame_index += 1

        pygame.display.update()

    def apply_update(self, update):
        if update == UPDATE_LEFT:
            self.gif_index = (self.gif_index - 1) % len(self.gifs)
        elif update == UPDATE_RIGHT:
            self.gif_index = (self.gif_index + 1) % len(self.gifs)
