import pygame
import numpy as np
from pheromone import Pheromone
from pyqtree import Index
from helpers import Text, Button
from tunnel_system import TunnelSystem
from colony import Colony

pygame.init()

pygame.display.set_icon(pygame.image.load("images\\icon.png"))
pygame.display.set_caption("Ants")

clock = pygame.time.Clock()

CAM_SPEED = 25

colonies = ["Black", "Red", "Purple"]

FORAGERS = 3
TUNNLERS = 5


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
        self.underground = False
        self.show_quadtree = False

        self.num_ants = [0, 0, 0]

        self.cam_x = 0
        self.cam_y = 0
        self.dt = 0  # Time between frames

        self.cam_m = np.zeros(2)

        self.d_width = 1700
        self.d_height = 950

        self.w_width = 750
        self.w_height = 750

        """Nest list"""
        self.food = []

        self.colonies = [Colony(self, 0, (100, 100), FORAGERS, TUNNLERS),
                         Colony(self, 1, (self.w_width - 100, self.w_height - 100), FORAGERS, TUNNLERS),
                         Colony(self, 2, (100, self.w_height - 100), FORAGERS, TUNNLERS)]

        self.ants_killed = {0: 0,
                       1: 0,
                       2: 0}
        yspace = 25
        self.stats_text = [Text(self.d_width - 300, self.d_height - 100, "     Colony: Lost | Has", black, 30, "r"),
                           Text(self.d_width - 300, self.d_height - 100 + yspace, "Colony 1: " + str(self.ants_killed[0]), black, 30, "r"),
                           Text(self.d_width - 300, self.d_height - 100 + yspace * 2, "Colony 2: " + str(self.ants_killed[1]), black, 30, "r"),
                           Text(self.d_width - 300, self.d_height - 100 + yspace * 3, "Colony 3: " + str(self.ants_killed[2]), black, 30, "r"),
                           ]

        """Tunnel stuff"""
        self.tunnel_system = TunnelSystem(self)

        self.gameDisplay = pygame.display.set_mode((self.d_width, self.d_height))

        # self.ant_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        # self.ground_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        # self.pheromone_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        #
        # self.ui_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        #
        # self.underground_ant_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        # self.underground_ground_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        # self.underground_entrance_point_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)
        #
        # self.debug_layer = pygame.Surface((self.d_width, self.d_height), pygame.SRCALPHA)

        self.food_pheromones = Pheromone("food", self)
        self.fight_pheromones = Pheromone("fight", self)

        self.fps_counter = Text(20, 20, "", (128, 128, 0), 20, "right")

        self.toggle_underground_button = Button(self.gameDisplay, [self.d_width - 150, 0, 150, 50], "Toggle View",
                                                (0, 0, 0), 25, self.toggle_underground, (0, 0, 200), (0, 0, 255))
        self.toggle_quadtree_button = Button(self.gameDisplay, [self.d_width - 150, 50, 150, 50], "Toggle Quadtree",
                                                (0, 0, 0), 25, self.toggle_show_quadtree, (0, 200, 0), (0, 255, 0))


    def toggle_underground(self):
        self.underground = not self.underground

    def toggle_show_quadtree(self):
        self.show_quadtree = not self.show_quadtree

    def reset_layers(self):
        # self.debug_layer.fill(black)
        # self.ant_layer.fill(black)
        # self.pheromone_layer.fill(black)
        # self.ground_layer.fill(black)
        # self.ui_layer.fill(black)
        #
        # self.underground_ant_layer.fill(black)
        # self.underground_ground_layer.fill(black)
        # self.underground_entrance_point_layer.fill(black)

        if self.underground:
            self.gameDisplay.fill((53, 35, 21))
        else:
            self.gameDisplay.fill((255, 255, 255))

    def draw_world_boundaries(self):
        if not self.underground:
            pygame.draw.rect(self.gameDisplay, (255, 0, 0),
                             [0 - self.cam_x, 0 - self.cam_y, self.w_width, self.w_height], 4)
        else:
            pygame.draw.rect(self.gameDisplay, (255, 0, 0),
                             [0 - self.cam_x, 0 - self.cam_y, self.w_width, self.w_height],
                             4)

    def process_user_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
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

        self.cam_m = normalize(self.cam_m) * CAM_SPEED * self.dt

        self.cam_x += self.cam_m[0]
        self.cam_y += self.cam_m[1]

    def display_display(self):

        mouse = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        self.draw_world_boundaries()
        self.toggle_underground_button.update(mouse)
        self.toggle_quadtree_button.update(mouse)
        for i, t in enumerate(self.stats_text):
            if i > 0:
                t.set_text(colonies[i - 1] + " Colony: " + str(self.ants_killed[i - 1]) + " | " + str(self.num_ants[i - 1]))
            t.draw(self.gameDisplay)
        # if self.underground:
        #
        #     self.gameDisplay.blit(self.underground_ground_layer, (0, 0))
        #     self.gameDisplay.blit(self.underground_entrance_point_layer, (0, 0))
        #     # self.gameDisplay.blit(self.pheromone_layer, (0, 0))
        #     self.gameDisplay.blit(self.underground_ant_layer, (0, 0))
        # else:
        #     self.gameDisplay.blit(self.pheromone_layer, (0, 0))
        #     self.gameDisplay.blit(self.ground_layer, (0, 0))
        #     self.gameDisplay.blit(self.ant_layer, (0, 0))
        #     self.gameDisplay.blit(self.ui_layer, (0, 0))
            # self.gameDisplay.blit(self.debug_layer, (0, 0))
            self.fps_counter.set_text(str(int(clock.get_fps())))
            self.fps_counter.draw(self.gameDisplay)
        pygame.display.update()
        self.dt = clock.tick(6000) / 16
