
import pygame
from data.ui.button import Button
from data.ui.text import Text
from data.ui.caret import Caret

class TextButton(Button):
    def __init__(self,text="", font_size=24, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_object = Text(text=text, position=self.position, fg_color=self.fg_color)
        self.text_object.set_font_size(font_size)
        self.text_object.update_position(self.position.xy)
        self.is_pressed = False

    @property
    def left_click(self):
        if self.hovered and pygame.mouse.get_pressed()[0] and not self.parent.component_clicked: # TODO Should only run when click started on button
            return True
        return False

    @property
    def right_click(self):
        if self.hovered and pygame.mouse.get_pressed()[2] and not self.parent.component_clicked:
            return True
        return False

    def update(self):
        if self.position.xy != self.rect.topleft or self.size.xy != self.rect.size:
            self.rect.update(self.position.xy, self.rect.size)

        if self.left_click and not self.parent.component_clicked:
            self.parent.component_clicked = True  # TODO Not being set to True, by value and not reference?
            self.left_action()
        elif self.right_click and not self.parent.component_clicked:
            self.parent.component_clicked = True
            self.set_for_delete = True

        self.position.y = (self.size.y + self.padding) * self.id + self.margin_top

    def left_action(self):
        pass  # print("Doing action")

    def draw(self, surface):
        super().draw(surface)
        self.text_object.draw(surface)