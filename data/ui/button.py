from pygame import Surface, mouse, draw

from data.ui.text import Text
from data.ui.base import Base

class Button(Base):
    def __init__(self,r=0,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.r = r
        self.is_enabled = True

    @property
    def hovered(self):
        return self.rect.collidepoint(mouse.get_pos())

    @property
    def left_click(self):
        if self.hovered and mouse.get_pressed()[0]:
            return True
        return False

    @property
    def right_click(self):
        if self.hovered and mouse.get_pressed()[2]:
            return True
        return False

    def left_action(self):
        pass

    def right_action(self):
        pass

    def update(self):
        if self.position.xy != self.rect.topleft or self.size.xy != self.rect.size:
            self.rect.update(self.position.xy, self.rect.size)

        #if self.left_click and not self.parent.component_clicked:
        #    self.parent.component_clicked = True
        #    self.left_action()
        #elif self.right_click and not self.parent.component_clicked:
        #    self.parent.component_clicked = True

    def update_position(self, window_size):
        super().update_position(window_size)
        self.update()

    def center(self, surface):
        super().center(surface)
        self.update()

    def draw(self, surface):
        super().draw(surface)
        if self.hovered:
            surface.blit(self.hover_surface, self.position.xy)
            draw.rect(surface, self.fg_color.lerp((0,0,0), 0.2), self.surface.get_rect(topleft=self.position.xy), 1, self.r)
        else:
            surface.blit(self.surface, self.position.xy)
            draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, self.r)












