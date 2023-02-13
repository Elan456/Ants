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

FOOD_RESPAWN = True


def _loopallchildren(parent):
    for child in parent.children:
        if child.children:
            for subchild in _loopallchildren(child):
                yield subchild
        yield child


def update_food():
    old_food = game.food.copy()
    game.qFood = Index(bbox=[0, 0, game.w_width, game.w_height])
    for f in old_food:
        if not f.active:  # Remove the eaten food
            game.food.remove(f)
            if FOOD_RESPAWN:
                game.food.append(Food(game))
        else:
            game.qFood.insert(f, bbox=[f.x - f.radius, f.y - f.radius, f.x + f.radius, f.y + f.radius])

        f.draw(game)


def update_colonies():
    for c in game.colonies:
        c.draw_entrance_points(game)
        old_eps = c.entrance_points.copy()
        for e in old_eps:
            e.update()
            if not e.active:
                c.entrance_points.remove(e)

    game.num_ants = [0, 0, 0]
    for c in game.colonies:
        c.update(game)

def run_sim():
    t = 0
    while True:

        game.reset_layers()

        if game.underground:
            game.tunnel_system.draw(game)

        update_food()
        update_colonies()



        game.process_user_input_events()
        """Draw all the things that should be seen"""

        if game.show_quadtree:
            for c in _loopallchildren(game.colonies[0].qAnts):
                pygame.draw.rect(game.gameDisplay, (0, 255, 0),
                                 [c.center[0] - c.width / 2 - game.cam_x, c.center[1] - c.height / 2 - game.cam_y,
                                  c.width, c.height], 1)

        game.display_display()


cProfile.run("run_sim()", sort=2)
