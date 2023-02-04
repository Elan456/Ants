import pygame
from game import Game
from ant import *

d_width = 1000
d_height = 500

game = Game()

ANT_COUNT = 1


def run_sim():
    for _ in range(ANT_COUNT):
        game.lAnts.append(Forager(500, 500, 1))

    while True:
        game.reset_layers()
        for ant in game.lAnts:
            game.qAnts.insert(ant, bbox=[ant.x - .5, ant.y - .5, 1, 1])
            ant.draw(game)
        game.process_user_input_events()
        """Draw all the things that should be seen"""
        pygame.draw.circle(game.ant_layer, (255, 255, 255), (0, 0), 10)

        game.display_display()


run_sim()
