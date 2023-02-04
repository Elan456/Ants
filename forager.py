import math as m
import random
import pygame
from ant import Worker, center_rotate_blit, WORKER_IMAGE

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
        center_rotate_blit(game.ant_layer, WORKER_IMAGE, (self.x - game.cam_x, self.y - game.cam_y), m.degrees(self.direction + m.pi / 2))