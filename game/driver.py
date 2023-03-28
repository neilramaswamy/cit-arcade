# Example file showing a circle moving on screen
import pygame
from mapper.map import ensure_map
from leds.strip import get_strip, get_color
from threading import Thread, RLock
from webserve.webserve import do_webserve
from game.update import Update
import numpy as np
import os
import time
from config.config import config

Color = get_color()

# os.environ["SDL_VIDEODRIVER"] = "dummy"

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class CitArcadeGameDriver():
    def __init__(self, width: int, height: int, updates: list, updates_lock: RLock):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 32)

        self.image = pygame.image.load("game/assets/brown.png")
        self.image = pygame.transform.scale(self.image, (width, height))

        self.clock = pygame.time.Clock()
        self.player_pos = pygame.Vector2(1, 3)

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

        # # TODO(neil): Fix this coordinate hack!
        # pygame.draw.circle(self.screen, (0, 255, 0), (int(self.player_pos.x), int(self.player_pos.y)), 2)
        # pygame.display.update()

        self.screen.blit(self.image, (int(self.player_pos.x), int(self.player_pos.y)))
        pygame.display.update()

        arr = pygame.surfarray.array3d(self.screen)
        tarr = np.transpose(arr, axes=(1, 0, 2))

        return tarr

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
    err = False
    for i in range(len(rm_pixels)):
        row = rm_pixels[i]
        for j in range(len(row)):
            rm_index = (i * len(row)) + j
            if rm_index not in mapping:
                err = True
                print(f"Index {rm_index} not in mapping")
                continue
            else:
                strip_index = mapping[rm_index]

            pixel = rm_pixels[i][j]

            strip.setPixelColor(strip_index, Color(int(pixel[0]), int(pixel[1]), int(pixel[2])))

    if err:
        raise Exception("foo")
    strip.show()


if __name__ == "__main__":
    strip = get_strip()
    mapping = ensure_map()

    updates = []
    updates_lock = RLock()

    event_thread = Thread(name="webserve", target=do_webserve, args=(updates, updates_lock))
    game = CitArcadeGameDriver(40, 40, updates, updates_lock)

    # Run event thread in background
    event_thread.start()

    while game.apply_updates():
        pixels = game.get_pixels()
        render_to_strip(strip, pixels, mapping)
        game.clock.tick(30)