# Example file showing a circle moving on screen
import pygame
from mapper.map import ensure_map
import time
from leds.strip import get_strip, get_color
from threading import Thread, RLock
import os

Color = get_color()

os.environ["SDL_VIDEODRIVER"] = "dummy"

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class CitArcadeGameDriver():
    def __init__(self, updates: list, updates_lock: RLock):
        pygame.init()
        self.screen = pygame.display.set_mode((10, 9))
        self.clock = pygame.time.Clock()
        self.player_pos = pygame.Vector2(4, 5)

        self.updates = updates
        self.updates_lock = updates_lock


    # updates is a list of custom-specified updates, since our updates don't come from Pygame
    # itself; they'll be coming over the network, probably
    #
    # Returns whether to continue running
    def apply_updates(self) -> bool:
        print("about to apply updates")

        self.updates_lock.acquire()
        should_continue = True 

        for update in updates:
            print(f"Applying update {update}")
            if update.stop:
                should_continue = False 
                break

            if update.dx != None:
                self.player_pos.x += update.dx
            if update.dy != None:
                self.player_pos.y += update.dy
        
        self.updates_lock.release()
        return should_continue 

    def get_pixels(self):
        self.screen.fill((0, 0, 255))

        pygame.draw.circle(self.screen, (255, 0, 0), (4, 4), 2)

        pygame.display.flip()

        return pygame.surfarray.array3d(self.screen)

class Update():
    def __init__(self, dx = 0, dy = 0, stop: bool = False):
        self.dx = dx
        self.dy = dy
        self.stop = stop

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

        time.sleep(0.01)

def render_to_strip(strip, rm_pixels, mapping):
    for i in range(len(rm_pixels)):
        row = rm_pixels[i]
        for j in range(len(row)):
            rm_index = (i * len(row)) + j
            strip_index = mapping[rm_index]

            pixel = rm_pixels[i][j]
            print(f"pixel {rm_index} is {pixel} (strip index {strip_index})")

            strip.setPixelColor(strip_index, Color(int(pixel[0]), int(pixel[1]), int(pixel[2])))
    
    strip.show()


if __name__ == "__main__":
    strip = get_strip()

    mapping = ensure_map()

    updates = [Update(dx = 1), Update(dx = 1)]
    updates_lock = RLock()

    event_thread = Thread(name="event_receive", target=event_receive_thread, args=(updates, updates_lock))
    game = CitArcadeGameDriver(updates, updates_lock)

    # Run event thread in background
    # event_thread.start()

    while game.apply_updates():
        pixels = game.get_pixels()
        print(f"pixels are {pixels}")

        render_to_strip(strip, pixels, mapping)
        time.sleep(2)
