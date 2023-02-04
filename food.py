import pygame
import random
import math

green = (178, 172, 136)


class Food:
    def __init__(self, game):
        self.x = random.randint(0, game.w_width)
        self.y = random.randint(0, game.w_height)
        self.size = random.randint(10.100)

    def draw_food(self, game):
        pygame.draw.circle(game.ground_layer, green, (self.x, self.y), math.sqrt(self.size))

    def eat_food(self, game):
        self.size -= 1
