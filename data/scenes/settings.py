from data.scenes.scene import Scene
import pygame
from data.ui.text import Text



class Settings(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.text = Text(text=str(self.__class__.__name__))
        self.bg_color = pygame.Color("black")
        self.fg_color = pygame.Color("white")
        self.text.set_size(54)

    def draw_background(self):
        self.game.screen.fill(self.bg_color)

    def draw_foreground(self):
        self.text.draw(self.game.screen)