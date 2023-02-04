import pygame
from game import Game
from food import Food
from ant import *
from nest import EntrancePoint
from pyqtree import Index

game = Game()

ANT_COUNT = 10
FOOD_COUNT = 50

def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child


def run_sim():
    game.entrance_points.append(EntrancePoint(game, 1, 700, 500))
    for _ in range(ANT_COUNT):
        game.lAnts.append(Forager(game.entrance_points[0].x,
                                  game.entrance_points[0].y,
                                  1))

    for _ in range(FOOD_COUNT):
        game.food.append(Food(game))

    while True:
        game.reset_layers()
        game.qAnts = Index(bbox=[0, 0, game.w_width, game.w_height], max_items=5)
        for ant in game.lAnts:
            game.qAnts.insert(ant, bbox=[ant.x - 1, ant.y - 1, ant.x + 1, ant.y + 1])
            ant.update(game.food_pheromones, game)
            ant.draw(game)

        game.food_pheromones.draw(game)

        for f in game.food:
            f.draw(game)

        for e in game.entrance_points:
            e.draw(game)

        game.process_user_input_events()
        """Draw all the things that should be seen"""
        pygame.draw.circle(game.ant_layer, (255, 255, 255), (0, 0), 10)

        for c in _loopallchildren(game.qAnts):
            pygame.draw.rect(game.ant_layer, (0, 255, 0),
                             [c.center[0] - c.width / 2, c.center[1] - c.height / 2, c.width, c.height], 1)

        game.display_display()


run_sim()
