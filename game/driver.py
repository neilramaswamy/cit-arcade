# Example file showing a circle moving on screen
import pygame
from mapper.map import ensure_map
import time
from leds.strip import get_strip, get_color
from threading import Thread, RLock
from concurrent import futures

from game.update import Update
import os
from config.config import config

from webserve.webserve import start_grpc 

Color = get_color()

os.environ["SDL_VIDEODRIVER"] = "dummy"

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class CitArcadeGameDriver():
    def __init__(self, updates: list, updates_lock: RLock):
        pygame.init()
        self.screen = pygame.display.set_mode((10, 9))
        self.clock = pygame.time.Clock()
        self.player_pos = pygame.Vector2(3, 4)

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
        self.screen.fill((0, 0, 255))

        # TODO(neil): Fix this coordinate hack!
        pygame.draw.circle(self.screen, (0, 255, 0), (int(self.player_pos.y), int(self.player_pos.x)), 2)

        arr = pygame.surfarray.array3d(self.screen)
        return arr

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
            strip_index = mapping[rm_index]

            pixel = rm_pixels[i][j]

            strip.setPixelColor(strip_index, Color(int(pixel[0]), int(pixel[1]), int(pixel[2])))

    strip.show()


if __name__ == "__main__":
    strip = get_strip()

    if config.get('is_dev'):
        num_pixels = strip.numPixels()
        # TODO(neil): This identity map will not work once we have multiple panels
        # 
        # Really, dev panels should snake as well so that we replicate the actual hardware, but
        # that requires more work from Zack
        mapping = { i: i for i in range(num_pixels)}
    else:
        mapping = ensure_map()

    updates = []
    updates_lock = RLock()

    grpc_thread = Thread(name="webserve-grpc", target=start_grpc, args=(updates, updates_lock))
    game = CitArcadeGameDriver(updates, updates_lock)

    # Run gRPC thread in background
    grpc_thread.start()

    while game.apply_updates():
        pixels = game.get_pixels()
        render_to_strip(strip, pixels, mapping)