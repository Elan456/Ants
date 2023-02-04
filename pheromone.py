import pygame

GRID_SIZE = 5

def color_from_strength(x):
    return (255, 255 - x * 2.55, 255 - x * 2.55)


class Pheromone:
    def __init__(self, type, game):
        self.type = type
        self.grid = [[0 for _ in range(game.w_width // GRID_SIZE)] for _ in range(game.w_height // GRID_SIZE)]

    def lay_down(self, x, y):
        tx = int((x + 15) / GRID_SIZE)
        ty = int((y + 15) / GRID_SIZE)
        try:
            if self.grid[ty][tx] < 95:
                self.grid[ty][tx] += 5
        except IndexError:
            print("!Warning!:", x, y,"is off the map")

    def draw(self, game):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                pygame.draw.rect(game.pheromone_layer, color_from_strength(self.grid[y][x]), [x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE])
