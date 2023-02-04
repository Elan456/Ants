import pygame
from game import Game

d_width = 1000
d_height = 500

game = Game()

def run_sim():
    while True:
        game.process_user_input_events()

        game.reset_layers()
        """Draw all the things that should be seen"""
        pygame.draw.circle(game.ant_layer, (255, 255, 255), (0, 0), 10)

        game.display_display()


run_sim()
