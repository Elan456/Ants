import math as m
import random
import pygame
from pyqtree import Index
from game import Game
from nest import EntrancePoint
from ant import House, center_rotate_blit, WORKER_IMAGE
from forager import Forager


class Tunneler(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
        self.state = "tunneling"
        self.hit_wall = False
        self.distance_stepped = 0
        self.tether = []
        self.holding_dirt = False
        self.personal_dig_direction = random.randint(0, 100) % (2 * m.pi)
        self.max_dig = random.randint(3, 6)

    def try_to_spawn_entrance_point(self, game):
        shortest_distance = float("inf")
        for e in game.entrance_points:
            distance = m.dist((self.x, self.y), (e.x, e.y))
            if distance < shortest_distance:
                shortest_distance = distance

        if shortest_distance > 200:
            game.entrance_points.append(EntrancePoint(game, self.colony, self.x, self.y))
            game.lAnts.append(Forager(self.x, self.y, self.colony))
            game.lAnts.append(Forager(self.x, self.y, self.colony))
            game.ulAnts.append(Tunneler(self.x, self.y, self.colony))

    def tunnel(self, game):
        """
        Will try to dig a tunnel ahead of them, otherwise will just move forwards
        """
        ahead = (self.x + m.cos(self.direction) * 5, self.y + m.sin(self.direction) * 5)

        if game.tunnel_system.is_open(ahead[0], ahead[1]):

            # Can move this way
            self.move(game.w_width, game.w_height)
        else:
            # Take the dirt
            self.try_to_spawn_entrance_point(game)
            self.max_dig -= 1
            self.holding_dirt = True
            game.tunnel_system.dig(ahead[0], ahead[1])

    def update(self, game):
        self.energy -= .1

        """
        Checking if we passed an entrance point to reset the tether
        """
        # print(self.state)

        for e in game.entrance_points:
            if e.colony == self.colony and m.dist((self.x, self.y), (e.x, e.y)) < 20:
                self.tether = []

        if self.state == "random":
            self.energy -= .1  # To stop from them building too big of a circle around every entrance point
            if not self.holding_dirt:
                self.direction += random.randint(-100, 100) / 200
                self.tunnel(game)
            else:
                self.state = "returning"

            """Trying to start actual tunneling towards the pheromones"""
            strongest = self.get_strongest_pheromones_in_front(game, game.food_pheromones, half_width=20)
            if strongest is not None:
                self.state = "tunneling"

        if self.state == "tunneling":
            strongest = self.get_strongest_pheromones_in_front(game, game.food_pheromones, half_width=20)
            if strongest is None:
                self.state = "random"
            else:
                self.direction = m.atan2(strongest.y - self.y, strongest.x - self.x)


            # self.move(game.w_width, game.w_height)
            # self.direction = self.personal_dig_direction
            # if self.max_dig < 1:  # We've dug as far as we should in this direction
            #     self.personal_dig_direction = random.randint(0, 100) % (2 * m.pi)
            #     self.max_dig = random.randint(3, 6)

            """Tunnels if not holding dirt otherwise goes into return state"""

            # pygame.draw.circle(game.debug_layer, (0, 255, 255), (self.x - game.cam_x, self.y - game.cam_y), 2)
            if not self.holding_dirt:

                self.tunnel(game)
            else:
                self.state = "returning"

        if self.state == "returning":
            # pygame.draw.circle(game.debug_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y), 2)

            if len(self.tether) < 1:
                """Made it back to the nest"""
                # self.state = "tunneling"
                self.energy = 100
                self.distance_stepped = 0
                self.tether = []
                self.state = "tunneling"
                self.holding_dirt = False
            else:
                nx, ny = self.tether[-1]
                self.direction = m.atan2(ny - self.y, nx - self.x)
                self.x, self.y = nx, ny
                self.tether.pop(-1)

        else:
            """Tether connects them to the last entrance point they have been near"""
            self.tether.append((self.x, self.y))
            self.distance_stepped += 1
            if self.distance_stepped > self.energy * 10 + 10:
                # Start returning
                self.state = "returning"
