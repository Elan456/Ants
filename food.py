import pygame
import random
import math

green = (35, 150, 35)


class Food:
    def __init__(self, game):
        self.x = random.randint(25, game.w_width - 25)
        self.y = random.randint(25, game.w_height - 25)
        self.size = random.randint(500, 2000)
        self.radius = math.sqrt(self.size)
        self.active = True

    def draw(self, game):
        if self.active:
            pygame.draw.circle(game.ground_layer, green, (self.x - game.cam_x, self.y - game.cam_y), math.sqrt(self.size))
            pygame.draw.circle(game.ground_layer, (165, 42, 42), (self.x - game.cam_x, self.y - game.cam_y),
                               math.sqrt(self.size), width=5)

    def eat(self):
        self.size -= 100
        if self.size > 0:
            self.radius = math.sqrt(self.size)


        if self.size < 10:
            self.radius = 0
            self.active = False
