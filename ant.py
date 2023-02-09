import math
import random

import pygame
import numpy as np
import math as m

WARRIOR_IMAGE = pygame.image.load("images\\Soldier_Ant.png")
WARRIOR_IMAGE = pygame.transform.scale(WARRIOR_IMAGE, (20, 30))
RED_WARRIOR_IMAGE = pygame.image.load("images\\Red_Soldier_Ant.png")
RED_WARRIOR_IMAGE = pygame.transform.scale(RED_WARRIOR_IMAGE, (20, 30))
PURPLE_WARRIOR_IMAGE = pygame.image.load("images\\Purple_Soldier_Ant.png")
PURPLE_WARRIOR_IMAGE = pygame.transform.scale(PURPLE_WARRIOR_IMAGE, (20, 30))

QUEEN_IMAGE = pygame.image.load("images\\Queen_Ant.png")
RED_QUEEN_IMAGE = pygame.image.load("images\\Red_Queen_Ant.png")
PURPLE_QUEEN_IMAGE = pygame.image.load("images\\Purple_Queen_Ant.png")

WORKER_IMAGE = pygame.image.load("images\\Worker_Ant.png")
WORKER_IMAGE = pygame.transform.scale(WORKER_IMAGE, (12, 20))
RED_WORKER_IMAGE = pygame.image.load("images\\Red_Worker_Ant.png")
RED_WORKER_IMAGE = pygame.transform.scale(RED_WORKER_IMAGE, (12, 20))
PURPLE_WORKER_IMAGE = pygame.image.load("images\\Purple_Worker_Ant.png")
PURPLE_WORKER_IMAGE = pygame.transform.scale(PURPLE_WORKER_IMAGE, (12, 20))

worker_images = [WORKER_IMAGE, RED_WORKER_IMAGE, PURPLE_WORKER_IMAGE]
warrior_images = [WARRIOR_IMAGE, RED_WARRIOR_IMAGE, PURPLE_WARRIOR_IMAGE]


def center_rotate_blit(surface, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, -1 * angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)

    surface.blit(rotated_image, new_rect)


def normalize(x):
    magnitude = np.linalg.norm(x)
    if magnitude > 0:
        return x / np.linalg.norm(x)
    else:
        return np.zeros(2)


# THIS FUNCTION IS USING A LOT OF TIME TRY TO OPTIMIZE CALLED A LOT
def check_if_in_front(my_loc, target_loc, my_direction):
    direction_to_target = m.atan2(target_loc[1] - my_loc[1], target_loc[0] - my_loc[0])
    diff = abs(my_direction - direction_to_target)
    if diff > m.pi:
        diff = 2 * m.pi - diff

    return diff < m.pi / 2


class Ant:
    def __init__(self, x, y, colony, direction=None, speed=1, energy=0, food=0, health=100):
        if energy == 0:
            self.energy = random.randint(50, 200)
        self.colony = colony
        self.speed = speed
        if direction is None:
            self.direction = random.randrange(0, 100) / (2 * m.pi)
        self.health = health
        self.food = food

        self.color = (0, 0, 0)
        self.y = y
        self.x = x

        self.active = True

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

    def enemy_near_by(self, game, underground):
        return False
        qBox = [self.x - 50, self.y - 50, self.x + 50, self.y + 50]
        # pygame.draw.rect(game.debug_layer, (0, 0, 255), [self.x - 50, self.y - 50, 100, 100], 1)
        if underground:
            nears = game.uQAnts.intersect(qBox)
        else:
            nears = game.qAnts.intersect(qBox)

        for a in nears:
            if a.colony != self.colony:
                # Found an enemy any
                return True
        return False

    @staticmethod
    def get_strongest(pheromones):
        strongest = pheromones[0]
        for i in pheromones:
            if i.strength > strongest.strength:
                strongest = i
        return strongest

    def get_strongest_pheromones_in_front(self, game, in_pheromone_system=None, half_width=10):
        if in_pheromone_system is None:
            pheromone_system = game.food_pheromones
        else:
            pheromone_system = in_pheromone_system

        qBox = [self.x - half_width, self.y - half_width, self.x + half_width, self.y + half_width]
        pygame.draw.rect(game.debug_layer, (255, 0, 0),
                         [self.x - half_width - game.cam_x, self.y - half_width - game.cam_y, half_width * 2,
                          half_width * 2], 1)
        test_pheromones = pheromone_system.grid.intersect(bbox=qBox)

        in_front_pheromones = []
        for p in test_pheromones:
            if check_if_in_front(np.array([self.x, self.y]), np.array([p.x, p.y]), self.direction):
                in_front_pheromones.append(p)

        if len(in_front_pheromones) > 0:
            strongest = self.get_strongest(in_front_pheromones)
            return strongest
        else:
            return None

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
        # pygame.draw.circle(game.underground_ant_layer, (0, 255, 255), (self.x - game.cam_x, self.y - game.cam_y), 3)
        # pygame.draw.line(game.underground_ant_layer, (0, 255, 0), (self.x - game.cam_x, self.y - game.cam_y),
        #                  (self.x + m.cos(self.direction) * 10 - game.cam_x,
        #                   self.y + m.sin(self.direction) * 10 - game.cam_y))
        center_rotate_blit(game.underground_ant_layer, worker_images[self.colony],
                           (self.x - 5 - game.cam_x, self.y - 10 - game.cam_y),
                           m.degrees(self.direction + m.pi / 2))


class Nurse(House):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony)
