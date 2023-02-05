import pygame
from game import Game
from food import Food
from ant import *
from forager import Forager
from nest import EntrancePoint
from pyqtree import Index
from tunneler import Tunneler

game = Game()

ANT_COUNT = 25
FOOD_COUNT = 100

def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child


def run_sim():
    game.entrance_points.append(EntrancePoint(game, 0, 400, 400))
    # game.entrance_points.append(EntrancePoint(game, 1, 800, 400))
    for _ in range(ANT_COUNT):
        game.lAnts.append(Forager(game.entrance_points[0].x,
                                  game.entrance_points[0].y,
                                  0))

    for _ in range(ANT_COUNT - 15):
        game.ulAnts.append(Tunneler(game.entrance_points[0].x,
                                    game.entrance_points[0].y, 0))

    for _ in range(FOOD_COUNT):
        game.food.append(Food(game))

    while True:
        game.reset_layers()
        game.qAnts = Index(bbox=[0, 0, game.w_width, game.w_height], max_items=5)

        for ant in game.lAnts:
            game.qAnts.insert(ant, bbox=[ant.x - 1, ant.y - 1, ant.x + 1, ant.y + 1])
            ant.update(game.food_pheromones, game)
            if not game.underground:
                ant.draw(game)

        for ant in game.ulAnts:
            ant.update(game)
            if game.underground:
                ant.draw(game)

        game.food_pheromones.update(game, do_draw=True)

        for f in game.food:
            f.draw(game)

        for e in game.entrance_points:
            e.draw(game)

        game.tunnel_system.draw(game)

        game.process_user_input_events()
        """Draw all the things that should be seen"""

        for c in _loopallchildren(game.qAnts):
            pygame.draw.rect(game.ant_layer, (0, 255, 0),
                             [c.center[0] - c.width / 2, c.center[1] - c.height / 2, c.width, c.height], 1)

        game.display_display()


run_sim()
