import pygame
from data.constants import SCREEN_SIZE
from data.ui.Font import Font

class Text:
    def __init__(self,
                 text="None",
                 color=pygame.Color("white"),
                 position=(0, 0),
                 center_x=False,
                 center_y=False,
                 ):
        self.text = text
        self.rendered_text = None
        self.color = color
        self.x, self.y = position
        self.center_x = center_x
        self.center_y = center_y
        self.size = (0, 0)
        self.font = Font()
        self.update()

    def update(self):
        self.size = self.font.get_rendered_size(self.text)
        if self.center_x:
            self.x = SCREEN_SIZE[0] / 2 - self.size[0] / 2
        if self.center_y:
            self.y = SCREEN_SIZE[1] / 2 - self.size[1] / 2
        self.rendered_text = self.font.render(self.text, self.color)

    def _center(self, surface, obj):
        surf_x, surf_y = surface.get_width() / 2, surface.get_height() / 2
        x, y = obj.get_width() / 2, obj.get_height() / 2
        surface.blit(obj, (surf_x - x, surf_y - y))

    def draw(self, surface):
        if self.center_x and self.center_y:
            self._center(surface, self.rendered_text)
        else:
            surface.blit(self.rendered_text, (self.x, self.y))

    def change_text(self, text):
        self.text = text
        self.update()

    def get_width(self):
        return self.rendered_text.get_width()

    def get_height(self):
        return self.rendered_text.get_height()
