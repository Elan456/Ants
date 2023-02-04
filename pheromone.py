import pygame


class Pheromone:
    def __init__(self, x, y, type):
        self.y = y
        self.x = x
        self.type = type
        self.previous = None
        self.next = None
        self.strength = 100
        self.active = True

        if self.type == "fight":
            self.color = (255, 0, 0)
        elif self.type == "food":
            self.color = (0, 255, 0)
        elif self.type == "home":
            self.color = (0, 0, 255)

    def update(self):
        self.strength -= 1
        if self.strength <= 0:
            self.active = False

    def draw(self, game):
        pygame.draw.circle(game.pheromone_layer, self.color, (self.x, self.y), 3)
