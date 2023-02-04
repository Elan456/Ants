import pygame
import numpy as np
from pheromone import Pheromone
from pyqtree import Index
from helpers import Text

pygame.init()

clock = pygame.time.Clock()

def normalize(x):
    magnitude = np.linalg.norm(x)
    if magnitude > 0:
        return x / np.linalg.norm(x)
    else:
        return np.zeros(2)


black = (0, 0, 0, 0)


class Game:
    """
    Hold game global variables that will be used everywhere pretty much handles drawings
    """

    def __init__(self):

        self.cam_x = 0
        self.cam_y = 0

        self.cam_m = np.zeros(2)

        self.d_width = 1500
        self.d_height = 900

        self.w_width = 800
        self.w_height = 800

        """Nest list"""
        self.entrance_points = []

        self.food = []

        """List of all the ants"""
        self.lAnts = []

        """The quadtree for all the ants"""
        self.qAnts = Index(bbox=[0, 0, self.w_width, self.w_height])

        self.gameDisplay = pygame.display.set_mode((self.d_width, self.d_height))

        self.ant_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        self.ground_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        self.pheromone_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)

        self.food_pheromones = Pheromone("food", self)
        self.fight_pheromones = Pheromone("fight", self)

        self.fps_counter = Text(20, 20, "", (128, 128, 0), 20, "right")

    def reset_layers(self):
        self.ant_layer.fill(black)
        self.pheromone_layer.fill(black)
        self.ground_layer.fill(black)
        self.gameDisplay.fill((255, 255, 255))

    def draw_world_boundaries(self):
        pygame.draw.rect(self.ground_layer, (255, 0, 0), [0, 0, self.w_width, self.w_height], 4)

    def process_user_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        self.cam_m = np.zeros(2)

        if keys[pygame.K_UP]:
            self.cam_m[1] -= 1
        if keys[pygame.K_DOWN]:
            self.cam_m[1] += 1
        if keys[pygame.K_RIGHT]:
            self.cam_m[0] += 1
        if keys[pygame.K_LEFT]:
            self.cam_m[0] -= 1

        self.cam_m = normalize(self.cam_m)

        self.cam_x += self.cam_m[0]
        self.cam_y += self.cam_m[1]

    def display_display(self):
        self.draw_world_boundaries()
        self.gameDisplay.blit(self.pheromone_layer, (-1 * self.cam_x, -1 * self.cam_y))
        self.gameDisplay.blit(self.ground_layer, (-1 * self.cam_x, -1 * self.cam_y))
        self.gameDisplay.blit(self.ant_layer, (-1 * self.cam_x, -1 * self.cam_y))
        self.fps_counter.set_text(str(int(clock.get_fps())))
        self.fps_counter.draw(self.gameDisplay)
        pygame.display.update()
        clock.tick(60)
