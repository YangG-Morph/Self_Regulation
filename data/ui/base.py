import pygame
from pygame.math import Vector2
from copy import deepcopy


class Base:
    margin = 30
    padding = 10

    def __init__(self,
                 size=(10, 10),
                 position=(0, 0),
                 bg_color=pygame.Color("black"),
                 fg_color=pygame.Color("white"),
                 center_x=False,
                 center_y=False,
                 align_left=False,
                 align_right=False,
                 align_top=False,
                 align_bottom=False,
                 parent=None,
                 visible=True,
                 background_image=None,
                 margin=30,
                 ):
        self.size = Vector2(size)
        self.position = Vector2(position)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.center_x = center_x
        self.center_y = center_y
        self.surface = pygame.Surface(self.size).convert_alpha()
        self.surface.fill(bg_color)
        self.hover_surface = pygame.Surface(self.size).convert_alpha()
        self.hover_surface.fill(bg_color.lerp((255, 255, 255), 0.1))
        self.rect = self.surface.get_rect(center=self.position.xy)
        self.align_left = align_left  # Align to parent's size
        self.align_right = align_right  # Align to parent's size
        self.align_top = align_top  # Align to parent's size
        self.align_bottom = align_bottom  # Align to parent's size
        self.parent = parent  # No parent is window size
        self.id = 0
        self.visible = visible
        self.set_for_delete = False
        self.background_image = background_image
        self.stretched_background_image = background_image
        self.margin = margin

    def _center_both(self, window_size):
        self.position.xy = window_size[0] / 2 - self.size[0] / 2, window_size[1] / 2 - self.size[1] / 2

    def _center_x(self, window_size):
        self.position.x = window_size[0] / 2 - self.size[0] / 2

    def _center_y(self, window_size):
        self.position.y = window_size[1] / 2 - self.size[1] / 2

    def center(self, window_size):
        if self.center_x and self.center_y:
            self._center_both(window_size)
        elif self.center_x:
            self._center_x(window_size)
        elif self.center_y:
            self._center_y(window_size)
        if self.position.x < self.margin:
            self.position.x = self.margin
        elif self.position.x > self.margin:
            self.position.x = window_size[0] - self.margin
        if self.position.y > window_size[1]:
            self.position.y = window_size[1] - self.margin
        elif self.position.y < self.margin:
            self.position.y = self.margin

        if self.background_image:
            self.stretched_background_image = pygame.transform.smoothscale(self.background_image, window_size)
        self.size.x = self.parent.size.x / 2
        self.rebuild_surface()
        self.position.y = (self.size.y + self.padding) * self.id + self.margin

    def rebuild_surface(self):
        self.surface = pygame.Surface(self.size).convert_alpha()
        self.surface.fill(self.bg_color)
        self.hover_surface = pygame.Surface(self.size).convert_alpha()
        self.hover_surface.fill(self.bg_color.lerp((255, 255, 255), 0.1))
        self.rect = self.surface.get_rect(center=self.position.xy)

    def update_position(self, window_size):
        self.center(window_size)

    def draw(self, surface):
        if self.background_image:
            surface.blit(self.stretched_background_image, (0, 0))



    def __copy__(self):
        pass
