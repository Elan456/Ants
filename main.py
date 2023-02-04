import pygame
from game import Game

d_width = 1000
d_height = 500

game = Game()


def run_sim():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game.reset_layers()
        """Draw all the things that should be seen"""
        game.display_display()


run_sim()
