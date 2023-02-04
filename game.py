import pygame

black = (0, 0, 0, 0)


class Game:
    """
    Hold game global variables that will be used everywhere pretty much handles drawings
    """

    def __init__(self):
        self.cam_x = 0
        self.cam_y = 0

        self.d_width = 1000
        self.d_height = 500

        self.w_width = 1200
        self.w_height = 700

        self.gameDisplay = pygame.display.set_mode((self.d_width, self.d_height))

        self.ant_layer = pygame.Surface((self.w_width, self.w_height), pygame.SRCALPHA)
        self.ground_layer = pygame.Surface((self.w_width, self.w_height), pygame.SRCALPHA)

    def reset_layers(self):
        self.ant_layer.fill(black)
        self.ground_layer.fill(black)
        self.gameDisplay.fill(black)

    def display_display(self):
        self.gameDisplay.blit(self.ground_layer, (self.cam_x, self.cam_y))
        self.gameDisplay.blit(self.ant_layer, (self.cam_x, self.cam_y))
        pygame.display.update()
