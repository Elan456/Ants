import pygame
from pyqtree import Index

GRID_SIZE = 5

def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child

def color_from_strength(x):
    return 255, 255 - x * 2.55, 255 - x * 2.55


class PheromoneGrid:
    def __init__(self):
        self.strength = 0


class Pheromone:
    def __init__(self, type, game):
        self.type = type
        # self.lGrid = [[0 for _ in range(game.w_width // GRID_SIZE)] for _ in range(game.w_height // GRID_SIZE)]
        self.grid = Index(bbox=[0, 0, game.w_width, game.w_height])

    def lay_down(self, x, y):
        tx = int((x + 15) / GRID_SIZE)
        ty = int((y + 15) / GRID_SIZE)
        l = self.grid.intersect(bbox=[tx, ty, tx + GRID_SIZE, ty + GRID_SIZE])
        if len(l) == 0:  # No pheromone there right now
            print("INSERT MADE")
            self.grid.insert(PheromoneGrid(), bbox=[tx, ty, tx + GRID_SIZE, ty + GRID_SIZE])
        else:
            if l[0].strength < 95:
                l[0].strength += 5

    def draw(self, game):
        # for y in range(len(self.grid)):
        #     for x in range(len(self.grid[0])):
        #         if self.grid[y][x] > 0:
        #             pygame.draw.rect(game.pheromone_layer, color_from_strength(self.grid[y][x]),
        #                              [x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE])

        for c in _loopallchildren(game.qAnts):
            pygame.draw.rect(game.ant_layer, (255, 0, 0),
                             [c.center[0] - c.width / 2, c.center[1] - c.height / 2, c.width, c.height], 1)