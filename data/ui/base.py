import pygame
from pygame.math import Vector2


class Base:
    def __init__(self,
                 size=(10, 10),
                 position=(0, 0),
                 bg_color=pygame.Color("black"),
                 fg_color=pygame.Color("white"),
                 center_x=False,
                 center_y=False,
                 ):
        self.size = Vector2(size)
        self.position = Vector2(position)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.center_x = center_x
        self.center_y = center_y

    def _center_x(self, window_size):
        self.position.x = window_size[0] / 2 - self.size[0] / 2

    def _center_y(self, window_size):
        self.position.y = window_size[1] / 2 - self.size[1] / 2

    def _center_both(self, window_size):
        self.position.xy = window_size[0] / 2 - self.size[0] / 2, window_size[1] / 2 - self.size[1] / 2

    def center(self, window_size):
        if self.center_x and self.center_y:
            self._center_both(window_size)
        elif self.center_x:
            self._center_x(window_size)
        elif self.center_y:
            self._center_y(window_size)

    def update_position(self, window_size):
        self.center(window_size)
