import pygame
import numpy as np
import math as m


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

    def __init__(self, x, y):
        super().__init__(x, y)

    def lay_eggs(self):
        """
        Spawn an egg
        Reduce energy by 10
        """
        self.energy -= 10


class Worker(Ant):
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
        """Drops a pheromone of a specfic type"""


class House(Worker):
    """These ants stay in the next always digging tunnels and tending to the eggs"""

    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Tunneler(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Nurses(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Foragers(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)


class Warriors(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
