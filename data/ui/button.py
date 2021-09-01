import pygame

from data.ui.text import Text
from data.ui.base import Base

class Button(Base):
    def __init__(self, text="Click me", *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.text = Text(text=text, position=kwargs["position"], fg_color=kwargs["fg_color"])
        self.text.set_size(12)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(kwargs["bg_color"])
        self.rect = self.surface.get_rect(center=self.position.xy)

    @property
    def collide(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    @property
    def pressed(self):
        if self.collide and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def update(self):
        self.text.position.xy = self.position.xy
        self.rect.update(self.position.xy, self.rect.size)

    def update_position(self, window_size):
        super().update_position(window_size)
        self.update()

    def center(self, surface):
        super().center(surface)
        self.update()

    def draw(self, surface):
        surface.blit(self.surface, self.position.xy)
        self.text.draw(surface)












