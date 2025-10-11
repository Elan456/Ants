import pygame
from fastquadtree import RectQuadTree

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
        self.grid = RectQuadTree((0, 0, game.w_width, game.w_height), capacity=25)

    def is_open(self, x, y):
        """
        Used to tell if a spot underground is open or not
        """
        x = int(x / GRID_SIZE) * GRID_SIZE
        y = int(y / GRID_SIZE) * GRID_SIZE
        l = len(self.grid.query((x - 5, y - 5, x + 5, y + 5)))
        return l > 0

    def dig(self, x, y):
        x = int(x / GRID_SIZE) * GRID_SIZE
        y = int(y / GRID_SIZE) * GRID_SIZE
        self.grid.insert(geom=(x - GRID_SIZE / 2, y - GRID_SIZE / 2,
                               x + GRID_SIZE / 2, y + GRID_SIZE / 2),
                               obj=Space(x, y))

    def draw(self, game):
        pass
        all_cells = self.grid.query((0, 0, game.w_width, game.w_height))

        for c in all_cells:
            _id, min_x, min_y, max_x, max_y = c
            pygame.draw.rect(game.gameDisplay, (154, 123, 79),
                             [min_x - game.cam_x, min_y - game.cam_y, GRID_SIZE, GRID_SIZE])