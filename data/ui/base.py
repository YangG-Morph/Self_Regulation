import pygame
from pygame.math import Vector2
from copy import deepcopy


class Base:
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
                 margin=0,
                 margin_top=0,
                 margin_left=0,
                 margin_right=0,
                 margin_bottom=0,
                 padding=0,
                 border=False,
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
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom
        self.padding = padding
        self.border = border
        self.start_pos = self.parent.position.xy if self.parent else (0, 0)
        self._set_margins()

    def _set_margins(self):
        for attribute in ["margin_top", "margin_left", "margin_right", "margin_bottom"]:
            if self.margin > 0 and getattr(self, attribute) == 0:
                setattr(self, attribute, self.margin)


    def _center_both(self, window_size):
        self.position.xy = window_size[0] / 2 - self.size[0] / 2, window_size[1] / 2 - self.size[1] / 2

    def _center_x(self, window_size):
        self.position.x = window_size[0] / 2 - self.size[0] / 2

    def _center_y(self, window_size):
        self.position.y = window_size[1] / 2 - self.size[1] / 2

    def center(self, window_size):
        self.start_pos = Vector2(0, 0) #self.parent.position.xy if self.parent else Vector2(0, 0)

        if self.center_x and self.center_y:
            self._center_both(window_size)
        elif self.center_x:
            self._center_x(window_size)
        elif self.center_y:
            self._center_y(window_size)

        if self.position.x < self.margin_left:
            self.position.x = self.margin_left + self.start_pos.x
        elif self.position.x > window_size[0]:
            self.position.x = window_size[0] - self.margin_right - self.start_pos[0]

        if self.position.y < self.margin_top:
            self.position.y = self.margin_top #+ self.start_pos.y
        elif self.position.y > window_size[1]:
            self.position.y = window_size[1] - self.margin_bottom - self.start_pos[1]


        if self.background_image:
            width = int(window_size.x)
            height = int(window_size.y)
            self.stretched_background_image = pygame.transform.smoothscale(self.background_image, (width, height))
        if self.parent:
            self.size.x = self.parent.size.x * 0.7 # TODO might not need, remove later

        self.rebuild_surface()

        if hasattr(self, "text_object"):
            self.text_object.position.xy = self.position.xy


    def rebuild_surface(self):
        self.surface = pygame.Surface(self.size).convert_alpha()
        self.surface.fill(self.bg_color)
        self.hover_surface = pygame.Surface(self.size).convert_alpha()
        self.hover_surface.fill(self.bg_color.lerp((255, 255, 255), 0.1))
        self.rect = self.surface.get_rect(center=self.position.xy)

    def update(self, delta_time):
        if self.position.xy != self.rect.topleft or self.size.xy != self.rect.size:
            self.rect.update(self.position.xy, self.rect.size)

    def update_position(self, window_size):
        self.center(window_size)

    def draw(self, surface):
        if self.background_image:
            surface.blit(self.stretched_background_image, (0, 0))

        if self.border:
            pygame.draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, 5)



    def __copy__(self):
        pass
