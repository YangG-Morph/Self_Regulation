
import pygame
from data.ui.button import Button
from data.ui.text import Text
from data.ui.caret import Caret

class TextButton(Button):
    def __init__(self,text="", font_size=24, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_object = Text(text=text, position=self.position, fg_color=self.fg_color, margin_left=10)
        self.text_object.set_font_size(font_size)
        self.is_pressed = False
        self.padding = 5


    def delete_self(self):
        self.set_for_delete = True

    def update(self, delta_time):
        super().update(delta_time)
        if self.left_click and not self.parent.component_clicked:
            self.parent.component_clicked = True
            if self.parent.parent:
                self.parent.parent.component_clicked = True
            self.left_action()
        elif self.right_click and not self.parent.component_clicked:
            self.parent.component_clicked = True
            if self.parent.parent:
                self.parent.parent.component_clicked = True
            self.right_action()

        self.position.y = (self.size.y + self.padding) * self.id + self.margin_top

    def update_position(self, window_size):
        super().update_position(window_size)
        self.text_object.position.x = self.position.x + self.text_object.margin_left
        self.text_object.position.y = self.position.y + (self.size.y + self.text_object.margin_top) / 8

    def left_action(self):
        pass

    def draw(self, surface):
        super().draw(surface)
        self.text_object.draw(surface)