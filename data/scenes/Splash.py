import pygame
from data.scenes.Scene import Scene
from data.ui.Text import Text



class Splash(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.text = Text(text="Self regulation")
        self.bg_color = pygame.Color("black")
        self.fg_color = pygame.Color("white")
        self.text.font.set_size = 120
        self.text.update()

    def draw_background(self):
        self.game.screen.fill(self.bg_color)

    def draw_foreground(self):
        self.text.draw(self.game.screen)

