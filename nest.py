import pygame
import random

blue = (0, 0, 255)

team_colors = [(0, 0, 255),
               (37, 154, 100)]


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
        pygame.draw.circle(game.ground_layer, team_colors[self.colony], (self.x - game.cam_x, self.y - game.cam_y), 25)
