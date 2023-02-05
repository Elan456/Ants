import pygame
from pyqtree import Index

GRID_SIZE = 25

class Space:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = GRID_SIZE
        self.h = GRID_SIZE


class TunnelSystem:
    def __init__(self, game):
        self.game = game
        self.grid = Index(bbox=[0, 0, game.w_width, game.w_height], max_items=25)

    def is_open(self, x, y):
        """
        Used to tell if a spot underground is open or not
        """
        x = int(x / GRID_SIZE) * GRID_SIZE
        y = int(y / GRID_SIZE) * GRID_SIZE
        l = len(self.grid.intersect(bbox=[x - 5, y - 5, x + 5, y + 5]))
        pygame.draw.circle(self.game.debug_layer, (255, 0, 0), (x - self.game.cam_x, y - self.game.cam_y), 5)
        return l > 0

    def dig(self, x, y):
        x = int(x / GRID_SIZE) * GRID_SIZE
        y = int(y / GRID_SIZE) * GRID_SIZE
        self.grid.insert(Space(x, y), bbox=[x - GRID_SIZE / 2, y - GRID_SIZE / 2,
                                            x + GRID_SIZE / 2, y + GRID_SIZE / 2])

    def draw(self, game):
        pass
        all_cells = self.grid.intersect(bbox=[0, 0, game.w_width, game.w_height])

        for c in all_cells:
            pygame.draw.rect(game.underground_ground_layer, (154, 123, 79),
                             [c.x - game.cam_x, c.y - game.cam_y, GRID_SIZE, GRID_SIZE])
