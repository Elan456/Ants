import pygame
import random

blue = (0, 0, 255)


class EntrancePoint:
    def __init__(self, game, colony, x=None, y=None):
        self.colony = colony
        if x is None or y is None:
            """Random location decision"""
            self.x = random.randint(0, game.w_width)
            self.y = random.randint(0, game.w_height)
        else:
            self.x = x
            self.y = y

    def draw(self, game):
        pygame.draw.circle(game.ground_layer, blue, (self.x, self.y), 25)
