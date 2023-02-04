import pygame
from game import Game
from food import Food
from ant import *



game = Game()

ANT_COUNT = 10
FOOD_COUNT = 3


def run_sim():
    for _ in range(ANT_COUNT):
        game.lAnts.append(Forager(500, 500, 1))

    for _ in range(FOOD_COUNT):
        game.food.append(Food(game))

    while True:
        game.reset_layers()
        for ant in game.lAnts:
            game.qAnts.insert(ant, bbox=[ant.x - .5, ant.y - .5, 1, 1])
            ant.update(game.food_pheromones, game)
            ant.draw(game)

        game.food_pheromones.draw(game)

        for f in game.food:
            f.draw(game)

        game.process_user_input_events()
        """Draw all the things that should be seen"""
        pygame.draw.circle(game.ant_layer, (255, 255, 255), (0, 0), 10)

        game.display_display()


run_sim()
