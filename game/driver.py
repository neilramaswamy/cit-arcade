# Example file showing a circle moving on screen
import pygame
from mapper.map import ensure_map
import time
from leds.strip import get_strip

# os.environ["SDL_VIDEODRIVER"] = "dummy"

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class CitArcadeGameDriver():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((9, 10))
        self.clock = pygame.time.Clock()
        self.running = True

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
    
    # updates is a list of custom-specified updates, since our updates don't come from Pygame
    # itself; they'll be coming over the network, probably
    #
    # Returns whether to continue running
    def apply_updates(self, updates) -> bool:
        for update in updates:
            if update.stop == 1:
                return False

            if update.dx != None:
                self.player_pos.x += update.dx
            if update.py != None:
                self.player_pos.y += update.y

        return True

    def paint(self):
        self.screen.fill((0, 0, 255))

        pygame.draw.circle(self.screen, "red", self.player_pos, 2)

        # flip() the display to paint
        pygame.display.flip()

        return pygame.surfarray.array3d(self.screen)

if __name__ == "__main__":
    mapping = ensure_map()
    
    strip = get_strip()
    strip.begin()

    game = CitArcadeGameDriver()
    updates = []

    while game.apply_updates(updates):
        rm_pixels = game.paint()

        for i in range(len(rm_pixels)):
            row = rm_pixels[i]
            for j in range(len(row)):
                rm_index = (i * len(row)) + j 
                strip_index = mapping[rm_index]

                pixel = rm_pixels[i][j]  / 255

                strip.setPixelColorRGB(strip_index, pixel[0], pixel[1], pixel[2])
        strip.show()

        time.sleep(1)


