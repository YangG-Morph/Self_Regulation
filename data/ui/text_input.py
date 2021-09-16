
import pygame
from data.ui.text import Text
from data.ui.base import Base
from data.ui.caret import Caret
from data.ui.text_button import TextButton
from data.ui.button import Button

class TextInput(Button):
    def __init__(self,text="", font_size=24, enter_press_action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_object = Text(text=text, position=self.position, fg_color=self.fg_color, margin_left=10)
        self.text_object.set_font_size(font_size)
        self.input_mode = False
        self.prev_text = text
        self.input_text = "Enter task here..."
        self.caret = Caret(pygame.Vector2(1, self.text_object.size.y))
        self.is_pressed = False
        self.enter_press_action = enter_press_action
        self.resizable = True

    def set_text(self, text):
        self.text_object.set_text(text)
        self.input_text = ""

    def update(self, delta_time):
        super().update(delta_time)

        if self.left_click and not self.parent.component_clicked:
            self.parent.component_clicked = True
            self.input_mode = True
            if self.input_text == "Enter task here...":
                self.input_text = ""
            self.caret.x = len(self.input_text)
            self.left_action()

        if self.prev_text != self.input_text:
            self.prev_text = self.input_text
            self.text_object.set_text(self.input_text)

    def update_position(self, window_size):
        super().update_position(window_size)
        self.text_object.position.x = self.position.x + self.text_object.margin_left
        self.text_object.position.y = self.position.y + (self.size.y + self.text_object.margin_top) / 8

    def draw(self, surface):
        super().draw(surface)
        self.text_object.draw(surface)
        if self.input_mode:
            index = self.caret.x
            x = self.text_object.font.get_rendered_size(self.input_text[0:index])[0]
            start_pos = self.text_object.position.x + x, self.text_object.position.y
            end_pos = self.text_object.position.x + x, self.text_object.position.y + self.caret.size.y
            pygame.draw.aaline(surface, self.fg_color, start_pos, end_pos)