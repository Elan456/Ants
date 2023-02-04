import math
import random

import pygame
import numpy as np
import math as m

WARRIOR_IMAGE = pygame.image.load("images\\Soldier_Ant.png")
QUEEN_IMAGE = pygame.image.load("images\\Queen_Ant.png")
WORKER_IMAGE = pygame.image.load("images\\Worker_Ant.png")


def center_rotate_blit(surface, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, -1 * angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)

    surface.blit(rotated_image, new_rect)


class Ant:
    def __init__(self, x, y, colony, direction=None, speed=1, energy=100, food=0, health=100):
        self.colony = colony
        self.speed = speed
        if direction is None:
            self.direction = random.randrange(0, 100) / (2 * m.pi)
        self.health = health
        self.food = food
        self.energy = energy
        self.y = y
        self.x = x

    def eat(self):
        if self.food > 0:
            self.food -= 1
            self.energy += 1


class Queen(Ant):

    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def lay_eggs(self):
        """
        Spawn an egg
        Reduce energy by 10
        """
        self.energy -= 10

    def draw(self, game):
        """Draws a queen ant at this location"""
        center_rotate_blit(game.ant_layer, QUEEN_IMAGE, (self.x, self.y), self.direction)


class Worker(Ant):
    """
    Abstract worker class
    """

    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def feed_friends(self, ants):
        """
        Find nearby friends that are hungry and feed them occurs when an ant has a surplus of food
        """
        pass

    def move(self, max_w, max_h):
        """Updates the position of the ant based on their direction and speed"""
        self.x += m.cos(self.direction) * self.speed
        self.y += m.sin(self.direction) * self.speed

        if self.x + 10 > max_w:
            self.x = max_w - 10
        elif self.x < 0:
            self.x = 0
        elif self.y + 16 > max_h:
            self.y = max_h - 16
        elif self.y < 0:
            self.y = 0

    def drop_pheromone(self, type):
        """Drops a pheromone of a specific type"""
        pass


class House(Worker):
    """These ants stay in the next always digging tunnels and tending to the eggs"""

    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def draw(self, game):
        """Draws a worker ant at this location"""
        center_rotate_blit(game.ant_layer, WORKER_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), self.direction)


class Tunneler(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Nurse(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Forager(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
        self.state = "searching"
        self.found_food = False
        self.distance_searched = 0
        self.tether = []

    def update(self, food_pheromone_grid, game):
        self.energy -= .1
        if self.state == "searching":
            """
                Keep track of how far /
                Check low energy /
                Check for strong pheromone nearby and start following it
                Check if it found food
            """
            self.tether.append((self.x, self.y))
            self.distance_searched += 1
            if self.distance_searched > self.energy * 10 + 10:
                # Start returning
                self.state = "returning"

            for f in game.food:
                if m.dist((self.x + 10, self.y + 16), (f.x, f.y)) < f.radius:
                    f.eat()
                    self.food += 10
                    self.found_food = True
                    self.state = "returning"

            # Movement
            self.direction += random.randrange(-100, 100, 1) / 1000
            pygame.draw.circle(game.ant_layer, (0, 0, 255), (self.x - game.cam_x, self.y - game.cam_y), 3)
            pygame.draw.line(game.ant_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y), (self.x + m.cos(self.direction) * 10 - game.cam_x,
                                                                             self.y + m.sin(self.direction) * 10- game.cam_y))
            self.move(game.w_width, game.w_height)

        if self.state == "returning":
            if len(self.tether) < 1:
                self.state = "done"
            else:
                if self.found_food:
                    food_pheromone_grid.lay_down(self.x, self.y)
                nx, ny = self.tether[-1]
                self.direction = m.atan2(ny - self.y, nx - self.x)
                self.x, self.y = nx, ny
                self.tether.pop(-1)

    def draw(self, game):
        center_rotate_blit(game.ant_layer, WORKER_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), math.degrees(self.direction + math.pi / 2))


class Warriors(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def draw(self, game):
        """Draws a warrior ant"""
        center_rotate_blit(game.ant_layer, WARRIOR_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), self.direction)
