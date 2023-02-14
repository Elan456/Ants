import pygame
import random
import math
import time

green = (35, 150, 35)


class Food:
    def __init__(self, game):
        found_spot = False
        max_size = 1000
        while not found_spot:
            if max_size > 50:
                max_size -= 50

            # print(max_size)

            self.size = random.randint(10, max_size)
            self.x = random.randint(25, game.w_width - 25)
            self.y = random.randint(25, game.w_height - 25)
            self.radius = math.sqrt(self.size)


            # Checking for overlap with other food
            # nearbys = game.qFood.intersect(bbox=[0, 0, game.w_width, game.w_height])
            nearbys = game.food.copy()
            found_spot = True  # Has to be proven false
            for f in nearbys:
                if math.dist((self.x, self.y), (f.x, f.y)) < self.radius + f.radius:
                    # Touching another food
                    found_spot = False
                    break

        self.active = True

    def draw(self, game):
        if self.active:
            pygame.draw.circle(game.gameDisplay, green, (self.x - game.cam_x, self.y - game.cam_y), math.sqrt(self.size))
            pygame.draw.circle(game.gameDisplay, (165, 42, 42), (self.x - game.cam_x, self.y - game.cam_y),
                               math.sqrt(self.size), width=5)

    def get_bbox(self):
        return [self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius]


    def eat(self):
        self.size -= 100
        if self.size > 0:
            self.radius = math.sqrt(self.size)


        if self.size < 10:
            self.radius = 0
            self.active = False
