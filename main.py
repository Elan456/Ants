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

ANT_COUNT = 300
FOOD_COUNT = 10
FOOD_RESPAWN = True


def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child


def run_sim():

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
                if FOOD_RESPAWN:
                    game.food.append(Food(game))
            f.draw(game)

        for c in game.colonies:
            c.draw_entrance_points(game)

        game.num_ants = [0, 0, 0]
        for c in game.colonies:
            c.update(game)


        game.process_user_input_events()
        """Draw all the things that should be seen"""

        if game.show_quadtree:
            for c in _loopallchildren(game.colonies[0].qAnts):
                pygame.draw.rect(game.gameDisplay, (0, 255, 0),
                                 [c.center[0] - c.width / 2 - game.cam_x, c.center[1] - c.height / 2 - game.cam_y,
                                  c.width, c.height], 1)

        game.display_display()




cProfile.run("run_sim()", sort=2)


