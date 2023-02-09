import cProfile
import io

import pygame
import profile
import pstats
from pstats import SortKey
from game import Game
from food import Food
from ant import *
from warrior import Warrior
from forager import Forager
from nest import EntrancePoint
from pyqtree import Index
from tunneler import Tunneler



game = Game()

ANT_COUNT = 20
FOOD_COUNT = 1


def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child


def run_sim():
    game.entrance_points.append(EntrancePoint(game, 0, 200, 200))
    game.entrance_points.append(EntrancePoint(game, 1, game.w_width - 200, game.w_height - 200))
    game.entrance_points.append(EntrancePoint(game, 2, 200, game.w_height - 200))
    for _ in range(ANT_COUNT):
        game.lAnts.append(Forager(game.entrance_points[0].x,
                                  game.entrance_points[0].y,
                                  0))
        game.lAnts.append(Forager(game.entrance_points[1].x,
                                  game.entrance_points[1].y,
                                  1))
        game.lAnts.append(Forager(game.entrance_points[2].x,
                                  game.entrance_points[2].y,
                                  2))

    for _ in range(ANT_COUNT - 15):
        game.ulAnts.append(Tunneler(game.entrance_points[0].x,
                                    game.entrance_points[0].y, 0))
        game.ulAnts.append(Tunneler(game.entrance_points[1].x,
                                    game.entrance_points[1].y, 1))
        game.ulAnts.append(Tunneler(game.entrance_points[2].x,
                                    game.entrance_points[2].y,
                                    2))

    for _ in range(FOOD_COUNT):
        game.food.append(Food(game))

    t = 0
    while True:

        game.reset_layers()

        game.food_pheromones.update(game, do_draw=not game.underground)
        game.fight_pheromones.update(game, do_draw=not game.underground)

        if game.underground:
            game.tunnel_system.draw(game)

        old_food = game.food.copy()
        for f in old_food:
            if not f.active:  # Remove the eaten food
                game.food.remove(f)
                game.food.append(Food(game))
            f.draw(game)

        for e in game.entrance_points:
            e.draw(game)


        game.qAnts = Index(bbox=[0, 0, game.w_width, game.w_height], max_items=5)

        old_ants = game.lAnts.copy()
        for ant in old_ants:
            game.qAnts.insert(ant, bbox=[ant.x - 1, ant.y - 1, ant.x + 1, ant.y + 1])
            ant.update(game)
            if not game.underground:
                ant.draw(game)
            if not ant.active:
                if not isinstance(ant, Warrior):
                    game.ants_killed[ant.colony] += 1
                # if isinstance(ant, Forager):
                #     print("Forage killed")
                game.lAnts.remove(ant)

        old_ulAnts = game.ulAnts.copy()
        for ant in old_ulAnts:
            ant.update(game)
            if game.underground:
                ant.draw(game)
            if not ant.active:
                game.ulAnts.remove(ant)







        game.process_user_input_events()
        """Draw all the things that should be seen"""

        if game.show_quadtree:
            for c in _loopallchildren(game.qAnts):
                pygame.draw.rect(game.gameDisplay, (0, 255, 0),
                                 [c.center[0] - c.width / 2 - game.cam_x, c.center[1] - c.height / 2 - game.cam_y,
                                  c.width, c.height], 1)

        game.display_display()




cProfile.run("run_sim()", sort=2)


