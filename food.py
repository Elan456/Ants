import pygame
import random
import math

green = (50, 255, 50)


class Food:
    def __init__(self, game):
        self.x = random.randint(0, game.w_width)
        self.y = random.randint(0, game.w_height)
        self.size = random.randint(50, 500)
        self.radius = math.sqrt(self.size)

    def draw(self, game):
        pygame.draw.circle(game.ground_layer, green, (self.x - game.cam_x, self.y - game.cam_y), math.sqrt(self.size))

    def eat(self):
        self.size -= 1
        self.radius = math.sqrt(self.size)
