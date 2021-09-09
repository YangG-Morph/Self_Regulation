

import pygame

from data.ui.base import Base

class Alarm(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def draw(self, surface):
        super().draw(surface)
        pygame.draw.circle(surface, self.fg_color, (self.rect.bottomleft[0] + self.size.y, self.rect.bottomleft[1]), self.size.y)
        #surface.blit(self.surface, self.position)





