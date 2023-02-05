import math as m
import random
import numpy as np
import pygame
from ant import Worker, center_rotate_blit

def normalize(x):
    magnitude = np.linalg.norm(x)
    if magnitude > 0:
        return x / np.linalg.norm(x)
    else:
        return np.zeros(2)


def check_if_in_front(my_loc, target_loc, my_direction):
    small_ahead = my_loc + my_direction
    small_behind = my_loc

    # D to target
    d = normalize(target_loc - my_loc)
    small_to_target = my_loc + d


    return m.dist(small_behind, small_to_target) > m.dist(small_ahead, small_to_target)


class Forager(Worker):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
        self.state = "searching"
        self.found_food = False
        self.distance_searched = 0
        self.tether = []
        self.turning_direction = 1

    def get_strongest_pheromones_in_front(self, game, food_pheromone_grid):
        qBox = [self.x - 10, self.y - 10, self.x + 10, self.y + 10]
        pygame.draw.rect(game.debug_layer, (255, 0, 0), [self.x - 10 - game.cam_x, self.y - 10 - game.cam_y, 20, 20], 1)
        test_pheromones = food_pheromone_grid.grid.intersect(bbox=qBox)
        my_direction = [m.cos(self.direction), m.sin(self.direction)]

        in_front_pheromones = []
        for p in test_pheromones:
            if check_if_in_front(np.array([self.x, self.y]), np.array([p.x, p.y]), my_direction):
                in_front_pheromones.append(p)

        if len(in_front_pheromones) > 0:
            strongest = self.get_strongest(in_front_pheromones)
            return strongest
        else:
            return None

    @staticmethod
    def get_strongest(pheromones):
        strongest = pheromones[0]
        for i in pheromones:
            if i.strength > strongest.strength:
                strongest = i
        return strongest

    def update(self, food_pheromone_grid, game):
        self.energy -= .1

        if self.state == "searching" or self.state == "following trail":
            self.tether.append((self.x, self.y))
            self.distance_searched += 1
            if self.distance_searched > self.energy * 10 + 10:
                # Start returning
                self.state = "returning"

            for f in game.food:
                if f.active:
                    # print("GOT FOOD")
                    d = m.dist((self.x, self.y), (f.x, f.y))

                    if d < f.radius:
                        f.eat()
                        self.food += 10
                        self.found_food = True
                        self.state = "returning"
                    elif d < 50:
                        self.direction = m.atan2(f.y - self.y, f.x - self.x)

        if self.state == "searching":
            """
                Keep track of how far /
                Check low energy /
                Check for strong pheromone nearby and start following it
                Check if it found food
            """

            """
                Checking if I found food
            """


            # Movement
            self.direction += random.randrange(0, 100, 1) / 1000 * self.turning_direction
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

        if self.state == "following trail":
            strongest = self.get_strongest_pheromones_in_front(game, food_pheromone_grid)
            if strongest is None:
                self.state = "searching"
            else:
                self.direction = m.atan2(strongest.y - self.y, strongest.x - self.x)
            self.move(game.w_width, game.w_height)


        if self.state == "returning":
            if len(self.tether) < 1 or m.dist((self.x, self.y), self.tether[0]) < 10:
                """Made it back to the nest"""
                self.state = "searching"
                self.energy = 100
                self.found_food = False
                self.distance_searched = 0
                self.tether = []
            else:
                if self.found_food:
                    food_pheromone_grid.lay_down(self.x, self.y)
                nx, ny = self.tether[-1]
                self.direction = m.atan2(ny - self.y, nx - self.x)
                self.x, self.y = nx, ny
                self.tether.pop(-1)

    def draw(self, game):
        pygame.draw.circle(game.ant_layer, (0, 255, 255), (self.x - game.cam_x, self.y - game.cam_y), 3)
        pygame.draw.line(game.ant_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y),
                         (self.x + m.cos(self.direction) * 10 - game.cam_x,
                          self.y + m.sin(self.direction) * 10 - game.cam_y))

        if self.found_food:
            pygame.draw.circle(game.ant_layer, (128, 128, 0), (self.x - game.cam_x, self.y - game.cam_y), 4)
        pass
        # center_rotate_blit(game.ant_layer, WORKER_IMAGE, (self.x - game.cam_x, self.y - game.cam_y),
        #                    m.degrees(self.direction + m.pi / 2))
