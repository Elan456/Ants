import pygame
import random
from ant import *
from forager import Forager
from warrior import Warrior
from tunneler import Tunneler

blue = (0, 0, 255)
tortilla = (154, 123, 79)

team_colors = [[(129, 133, 137), (0, 0, 0)],
               [(180, 84, 78), (70, 0, 0)],
               [(147, 112, 219), (75, 0, 130)]]


class EntrancePoint:
    def __init__(self, game, colony, x=None, y=None):
        self.food = 0
        self.colony = colony
        self.warrior_cooldown = 100
        self.last_visit = 0
        self.active = True
        if x is None or y is None:
            """Random location decision"""
            self.x = random.randint(0, game.w_width)
            self.y = random.randint(0, game.w_height)
        else:
            self.x = x
            self.y = y

        self.bColor, self.cColor = team_colors[colony.num]

    def spawn_worker(self):
        if self.food > 40:
            r = random.randint(1, 10)
            if r < 9:
                self.colony.above_ants.append(Forager(self.x, self.y, self.colony))
            else:
                self.colony.under_ants.append(Tunneler(self.x, self.y, self.colony))
            self.food -= 30

    def spawn_warrior(self, game, direction=None):
        if self.food > 10 and self.warrior_cooldown == 0:
            self.warrior_cooldown = 100
            new_warrior = Warrior(self.x, self.y, self.colony, False)
            if direction is not None:
                new_warrior.direction = direction
            self.colony.above_ants.append(new_warrior)
            self.food -= 10


    def update(self):
        if self.warrior_cooldown > 0:
            self.warrior_cooldown -= 1

        self.last_visit += 1

        if self.last_visit > 2000:
            self.active = False
            if len(self.colony.under_ants) > 0:
                self.colony.under_ants.pop(0)
            if len(self.colony.under_ants) > 0:
                self.colony.under_ants.pop(0)

    def draw(self, game):

        pygame.draw.circle(game.gameDisplay, self.bColor,
                           (self.x - game.cam_x, self.y - game.cam_y), 25)
        pygame.draw.circle(game.gameDisplay, self.cColor,
                           (self.x - game.cam_x, self.y - game.cam_y), 10)
