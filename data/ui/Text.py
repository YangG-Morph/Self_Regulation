import pygame
from data.constants import SCREEN_SIZE
from data.ui.Font import Font
from data.Point import Point


class Text:
    def __init__(self,
                 text="None",
                 color=pygame.Color("white"),
                 position=(0, 0),
                 center_x=False,
                 center_y=False,
                 ):
        self.text = text
        self.color = color
        self.position = Point(*position)
        self.center_x = center_x
        self.center_y = center_y
        self.size = (0, 0)
        self.font = Font()
        self.rendered_text = self.font.render(self.text, self.color)

    def update(self):
        self.size = self.font.get_rendered_size(self.text)
        self.rendered_text = self.font.render(self.text, self.color)

    def _center_x(self, surface):
        self.position.x = surface[0] / 2 - self.size[0] / 2

    def _center_y(self, surface):
        self.position.y = surface[1] / 2 - self.size[1] / 2

    def _center_both(self, surface):
        self.position.set(surface.get_width() / 2 - self.rendered_text.get_width() / 2,
                          surface.get_height() / 2 - self.rendered_text.get_height() / 2)

        print(self.position.x)

    def center(self, surface):
        if self.center_x and self.center_y:
            self._center_both(surface)
        if self.center_x:
            self._center_x(surface)
        if self.center_y:
            self._center_y(surface)

    def draw(self, surface):
        surface.blit(self.rendered_text, (self.position.x, self.position.y))

    def change_text(self, text):
        self.text = text
        self.update()

    def get_width(self):
        return self.rendered_text.get_width()

    def get_height(self):
        return self.rendered_text.get_height()
