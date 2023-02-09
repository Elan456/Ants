import pygame
import random

blue = (0, 0, 255)
tortilla = (154, 123, 79)

team_colors = [[(129, 133, 137), (0, 0, 0)],
               [(180, 84, 78), (70, 0, 0)],
               [(147, 112, 219), (75, 0, 130)]]


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

        self.bColor, self.cColor = team_colors[colony - 1]

    def draw(self, game):
        pygame.draw.circle(game.gameDisplay, self.bColor,
                           (self.x - game.cam_x, self.y - game.cam_y), 25)
        pygame.draw.circle(game.gameDisplay, self.cColor,
                           (self.x - game.cam_x, self.y - game.cam_y), 10)
