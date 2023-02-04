import pygame
import numpy as np
import math as m

WARRIOR_IMAGE = pygame.image.load("images\\Soldier_Ant.png")
QUEEN_IMAGE = pygame.image.load("images\\Queen_Ant.png")
WORKER_IMAGE = pygame.image.load("images\\Worker_Ant.png")


def center_rotate_blit(surface, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)

    surface.blit(rotated_image, new_rect)


class Ant:
    def __init__(self, x, y, colony, direction=0, speed=1, energy=100, food=0, health=100):
        self.colony = colony
        self.speed = speed
        self.direction = direction
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

    def move(self):
        """Updates the position of the ant based on their direction and speed"""
        self.x += m.cos(self.direction) * self.speed
        self.y += m.sin(self.direction) * self.speed

    def drop_pheromone(self, type):
        """Drops a pheromone of a specific type"""
        pass


class House(Worker):
    """These ants stay in the next always digging tunnels and tending to the eggs"""

    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def draw(self, game):
        """Draws a worker ant at this location"""
        center_rotate_blit(game.ant_layer, WORKER_IMAGE, (self.x, self.y), self.direction)


class Tunneler(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Nurse(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Forager(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def draw(self, game):
        center_rotate_blit(game.ant_layer, WORKER_IMAGE, (self.x, self.y), self.direction)

class Warriors(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)

    def draw(self, game):
        """Draws a warrior ant"""
        center_rotate_blit(game.ant_layer, WARRIOR_IMAGE, (self.x, self.y), self.direction)
