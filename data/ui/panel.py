import pygame
from data.ui.base import Base

class Panel(Base):
    margin = 30

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.surface = pygame.Surface(self.size.xy)
        self.surface.fill(kwargs["bg_color"])
        self.components = []

    def add(self, obj):
        self.components.append(obj)

    def update(self, window_size):
        pass

    def update_position(self, window_size):
        if self.size.x >= window_size[0]:
            self.size.x = window_size[0] - self.margin
        if self.size.y >= window_size[1]:
            self.size.y = window_size[1] - self.margin
        self.surface = pygame.Surface(self.size.xy)
        self.surface.fill(self.bg_color)
        self.position.x += self.margin / 2
        self.position.y += self.margin / 2
        [obj.update_position(window_size) for obj in self.components]

    def draw(self, surface):
        #surface.blit(self.surface, self.position.xy)
        pygame.draw.rect(surface, self.bg_color, self.surface.get_rect(topleft=self.position.xy), 1, 2)
        [obj.draw(surface) for obj in self.components]



