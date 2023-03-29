import pygame
from mapper.map import ensure_map
from leds.mux import Color, strip
from threading import Thread, RLock
from webserve.webserve import do_webserve
from game.update import Update
import numpy as np
import os
from config.config import config

# When set to "dummy", the PyGame window will not appear
os.environ["SDL_VIDEODRIVER"] = "dummy"

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class CitArcadeGameDriver():
    def __init__(self, height: int, width: int, updates: list, updates_lock: RLock):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 32)

        self.image = pygame.image.load("game/assets/logo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.clock = pygame.time.Clock()
        self.player_pos = pygame.Vector2(0, 0)

        self.updates = updates
        self.updates_lock = updates_lock


    # updates is a list of custom-specified updates, since our updates don't come from Pygame
    # itself; they'll be coming over the network, probably
    #
    # Returns whether to continue running
    def apply_updates(self) -> bool:
        self.updates_lock.acquire()
        should_continue = True

        while len(updates) > 0:
            update = updates.pop(0)
            print(f"Applying update {update}")

            if update.stop:
                should_continue = False
                break

            if update.dx != None:
                self.player_pos.x += update.dx
            if update.dy != None:
                self.player_pos.y += update.dy

        updates
        self.updates_lock.release()
        return should_continue

    def get_pixels(self):
        self.screen.fill((0, 0, 0))

        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.player_pos.x), int(self.player_pos.y)), 2)

        self.screen.blit(self.image, (int(self.player_pos.x), int(self.player_pos.y)))
        pygame.display.update()

        # For some reason, we get back transposed coordinates from surfarray, so we transpose here
        # to fix that.
        arr = pygame.surfarray.array3d(self.screen)
        return np.transpose(arr, axes=(1, 0, 2))

def event_receive_thread(updates: list, updates_lock: RLock):
    while True:
        command = input("Type (u/d/l/r/stop): ")

        update = None
        if command == "u":
            update = Update(dy = -1)
        elif command == "d":
            update = Update(dy = 1)
        elif command == "l":
            update = Update(dx = -1)
        elif command == "r":
            update = Update(dx = 1)
        elif command == "stop":
            update = Update(stop = True)

        updates_lock.acquire()
        updates.append(update)
        updates_lock.release()

def render_to_strip(strip, rm_pixels, mapping):
    for i in range(len(rm_pixels)):
        row = rm_pixels[i]
        for j in range(len(row)):
            rm_index = (i * len(row)) + j

            if rm_index not in mapping:
                raise Exception(f"Index {rm_index} is not in mapping: double check Game board dimensions or the map you're using.")
            else:
                strip_index = mapping[rm_index]

            pixel = rm_pixels[i][j]

            strip.setPixelColor(strip_index, Color(int(pixel[0]), int(pixel[1]), int(pixel[2])))
    strip.show()


if __name__ == "__main__":
    mapping = ensure_map()

    updates = []
    updates_lock = RLock()

    event_thread = Thread(name="webserve", target=do_webserve, args=(updates, updates_lock))
    game = CitArcadeGameDriver(40, 36, updates, updates_lock)

    # Run event thread in background
    event_thread.start()

    while game.apply_updates():
        pixels = game.get_pixels()
        render_to_strip(strip, pixels, mapping)
        game.clock.tick(30)