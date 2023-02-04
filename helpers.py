import pygame
class Text:
    def __init__(self, x, y, text, text_color, text_size, align="center"):
        self.align = align
        self.color = text_color
        self.font = pygame.font.SysFont(None, text_size)
        self.x = x
        self.y = y
        self.text = None
        self.set_text(text)

    def set_text(self, text):
        self.text = self.font.render(text, True, self.color)
        r = self.text.get_rect()
        if self.align == "center":
            self.x -= r.width / 2
            self.y -= r.height / 2

    def draw(self, surface):
        surface.blit(self.text, (self.x, self.y))