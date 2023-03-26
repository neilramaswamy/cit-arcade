# Example file showing a circle moving on screen
import pygame
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

# A remarkably simple game where we paint a red ball to the screen on top of a purple background.
class CitArcadeGameDriver():
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((36, 36))
        self.clock = pygame.time.Clock()
        self.running = True

        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
    
    # dx, dy of the ball
    def paint(self, dx, dy):
        self.screen.fill("purple")

        self.player_pos.y += dy
        self.player_pos.x += dx

        pygame.draw.circle(self.screen, "red", self.player_pos, 5)

        # flip() the display to paint
        pygame.display.flip()

        return pygame.surfarray.array3d(self.screen)