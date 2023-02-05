import pygame
import random

blue = (0, 0, 255)
tortilla = (154, 123, 79)

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
        if game.underground:
            pygame.draw.rect(game.underground_ground_layer, tortilla, [self.x - 75 - game.cam_x, self.y - 75 - game.cam_y, 150, 150])
            pygame.draw.circle(game.underground_ground_layer, blue, (self.x - game.cam_x, self.y - game.cam_y), 25)

        else:
            pygame.draw.circle(game.ground_layer, blue, (self.x - game.cam_x, self.y - game.cam_y), 25)
