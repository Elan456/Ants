import math as m
import random
import pygame
from pyqtree import Index
from game import Game
from ant import House, center_rotate_blit, WORKER_IMAGE

class Space:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.w = 25
        self.h = 25

class Tunneler(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
        self.state = "tunneling"
        self.hit_wall = False
        self.distance_tunneled = 0
        self.tether = []

    def update(self, game):
        self.energy -= .1
        if self.state == "tunneling":
            """
                Keep track of how far /
                Check low energy /
            """
            self.tether.append((self.x, self.y))
            self.distance_tunneled += 1
            if self.distance_tunneled > self.energy * 10 + 10:
                # Start returning
                self.state = "returning"

