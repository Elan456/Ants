import math as m
import random
import numpy as np
import pygame
from ant import Worker, center_rotate_blit, worker_images, normalize, check_if_in_front
from warrior import Warrior


class Forager(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
        self.state = "searching"
        self.found_food = False
        self.distance_searched = 0

        self.turning_direction = 1
        self.spooked = False
        self.near_food = False


    def check_food(self, game):
        closest_distance = float("inf")
        closest = None
        self.near_food = False
        for f in game.food:
            if f.active:
                # print("GOT FOOD")
                d = m.dist((self.x, self.y), (f.x, f.y))

                if d < f.radius:
                    f.eat()
                    self.food += 10  # Not used for anything
                    self.found_food = True
                    self.state = "returning"
                elif d < 50:
                    self.near_food = True
                    if d < closest_distance:
                        closest_distance = d
                        closest = f

        if self.near_food:
            self.direction = m.atan2(closest.y - self.y, closest.x - self.x)
            self.move(game.w_width, game.w_height)

    def update(self, game):
        food_pheromone_grid = game.food_pheromones
        self.energy -= .05

        self.try_reset_tether()

        """Check for spooked"""
        if self.enemy_near_by(game, False):
            self.spooked = True
            self.state = "returning"

        if self.state == "searching" or self.state == "following trail":

            self.tether.append((self.x, self.y))
            self.distance_searched += 1
            if self.distance_searched > self.energy * 10 + 10:
                # Start returning
                self.state = "returning"

        if not self.found_food:
            self.check_food(game)

        if self.state == "searching" and not self.near_food:
            """
                Check for strong pheromone nearby and start following it
                Check if it found food
            """

            # Movement
            self.direction += random.randrange(0, 100, 1) / 2000 * self.turning_direction
            if random.randint(0, 10) == 0:
                self.turning_direction *= -1

            self.move(game.w_width, game.w_height)

            """
            Checking for a pheromone trail to follow
            """
            strongest = self.get_strongest_pheromones_in_front(game, food_pheromone_grid)
            if strongest is not None and strongest.strength > 25:
                self.direction = m.atan2(strongest.y - self.y, strongest.x - self.x)
                self.state = "following trail"

        if self.state == "following trail" and not self.near_food:
            strongest = self.get_strongest_pheromones_in_front(game, food_pheromone_grid)
            if strongest is None:
                self.state = "searching"
            else:
                self.direction = m.atan2(strongest.y - self.y, strongest.x - self.x)
            self.move(game.w_width, game.w_height)

        if self.state == "returning":
            if len(self.tether) < 1:
                """Made it back to the nest"""
                self.state = "searching"
                self.energy = 100
                if self.found_food:
                    self.my_entrance_point.food += 10
                    self.my_entrance_point.spawn_forager(game)
                self.found_food = False
                self.distance_searched = 0

                if self.spooked:
                    # Spawn a warrior ant
                    self.my_entrance_point.spawn_warrior(game, self.direction + m.pi)
                self.direction += m.pi  # To face towards their own pheromone trail
                self.spooked = False
                # self.tether = []
            else:
                if self.found_food:
                    food_pheromone_grid.lay_down(self.x, self.y)
                elif self.spooked:
                    game.fight_pheromones.lay_down(self.x, self.y)
                nx, ny = self.tether[-1]
                self.direction = m.atan2(ny - self.y, nx - self.x)
                self.x, self.y = nx, ny
                self.tether.pop(-1)

    def draw(self, game):
        # pygame.draw.circle(game.ant_layer, (0, 255, 255), (self.x - game.cam_x, self.y - game.cam_y), 3)
        # pygame.draw.line(game.ant_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y),
        #                  (self.x + m.cos(self.direction) * 10 - game.cam_x,
        #                   self.y + m.sin(self.direction) * 10 - game.cam_y))

        center_rotate_blit(game.gameDisplay, worker_images[self.colony.num],
                           (self.x - 5 - game.cam_x, self.y - 10 - game.cam_y),
                           m.degrees(self.direction + m.pi / 2))

        if self.found_food:
            pygame.draw.circle(game.gameDisplay, (128, 128, 0), (self.x - game.cam_x, self.y - game.cam_y), 4)
