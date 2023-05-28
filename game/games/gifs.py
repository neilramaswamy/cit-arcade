import os

import pygame

from game.mini_game import AbstractMiniGame

FRAME_RATE = 24
FRAME_DELAY = (1000) / FRAME_RATE

NUM_LOOPS_PER_GIF = 10

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

        self.gifs = ["blueno", "sonic", "rainbow", "fireworks"]

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

        # End of current gif        
        if (self.frame_index == len(self.frames[self.gif_index]) - 1):
            self.frame_index = 0

            # Go to the next gif
            if self.loops_for_curr_gif == NUM_LOOPS_PER_GIF - 1:
                self.gif_index = (self.gif_index + 1) % len(self.gifs)
                self.loops_for_curr_gif = 0
            else:
                # Loop once more
                self.loops_for_curr_gif += 1
        else:
            self.frame_index += 1

        pygame.display.update()

    def apply_update(self, update=None):
        return