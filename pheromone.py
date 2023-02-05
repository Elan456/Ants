import pygame
from pyqtree import Index

GRID_SIZE = 5


def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child


def color_from_strength_red(x):
    return 255, 255 - x * 2.55, 255 - x * 2.55


def color_from_strength_blue(x):
    return 255 - x * 2.55, 255 - x * 2.55, 255


class PheromoneGrid:
    def __init__(self, x, y):
        self.strength = 10
        self.x = x
        self.y = y


class Pheromone:
    def __init__(self, type, game):
        self.type = type
        if self.type == "food":
            self.color_function = color_from_strength_red
        elif self.type == "fight":
            self.color_function = color_from_strength_blue
        # self.lGrid = [[0 for _ in range(game.w_width // GRID_SIZE)] for _ in range(game.w_height // GRID_SIZE)]
        self.grid = Index(bbox=[0, 0, game.w_width, game.w_height], max_items=10)

    def update(self, game, do_draw=False):
        all_cells = self.grid.intersect(bbox=[0, 0, game.w_width, game.w_height])
        self.grid = Index(bbox=[0, 0, game.w_width, game.w_height], max_items=10)
        for c in all_cells:
            c.strength -= .03
            if c.strength > 0:
                if do_draw:
                    pygame.draw.rect(game.pheromone_layer, self.color_function(c.strength),
                                     [c.x - game.cam_x, c.y - game.cam_y, GRID_SIZE, GRID_SIZE])
                self.grid.insert(c, bbox=[c.x, c.y, c.x + GRID_SIZE, c.y + GRID_SIZE])

    def lay_down(self, x, y):
        tx = int(x / GRID_SIZE) * GRID_SIZE
        ty = int(y / GRID_SIZE) * GRID_SIZE
        l = self.grid.intersect(bbox=[tx + 1, ty + 1, tx + GRID_SIZE - 1, ty + GRID_SIZE - 1])
        if len(l) == 0:  # No pheromone there right now
            self.grid.insert(PheromoneGrid(tx, ty), bbox=[tx, ty, tx + GRID_SIZE, ty + GRID_SIZE])
        else:
            if l[0].strength < 95:
                l[0].strength += 5

    def draw(self, game):
        pass
        # for y in range(len(self.grid)):
        #     for x in range(len(self.grid[0])):
        #         if self.grid[y][x] > 0:
        #             pygame.draw.rect(game.pheromone_layer, color_from_strength(self.grid[y][x]),
        #                              [x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE])
