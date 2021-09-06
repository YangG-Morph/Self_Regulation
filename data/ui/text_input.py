
import pygame
from data.ui.text import Text
from data.ui.base import Base
from data.ui.caret import Caret
from data.ui.text_button import TextButton

class TextInput(TextButton):
    def __init__(self,text="Not implemented", font_size=24, enter_press_action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_object = Text(text=text, position=self.position, fg_color=self.fg_color)
        self.text_object.set_font_size(font_size)
        self.text_object.update_position(self.position.xy)
        self.input_mode = False
        self.prev_text = text
        self.input_text = text
        self.original_text = text  # Store text_object when input started, restore when escape pressed
        self.caret = Caret(pygame.Vector2(1, self.text_object.size.y))
        self.is_pressed = False
        self.enter_press_action = enter_press_action

    @property
    def left_click(self):
        if self.hovered and pygame.mouse.get_pressed()[0] and not self.parent.component_clicked:  # TODO Should only run when click started on button
            return True
        return False

    def set_text(self, text):
        self.text_object.set_text(text)
        #self.prev_text = ""
        self.input_text = ""

    def update(self, manager=None):
        if self.position.xy != self.rect.topleft or self.size.xy != self.rect.size:
            self.rect.update(self.position.xy, self.rect.size)

        if self.left_click and not manager.component_clicked:
            manager.component_clicked = True
            self.input_mode = True
            self.caret.x = len(self.input_text)
            self.left_action()

        if self.prev_text != self.input_text:
            self.prev_text = self.input_text
            self.text_object.set_text(self.input_text)
        #print("Inside text_input: ", self.position, " and margin_top: ", self.margin_top)

    def left_action(self):
        pass  # print("Doing action")

    def draw(self, surface):
        super().draw(surface)
        self.text_object.draw(surface)
        if self.input_mode:
            index = self.caret.x#len(self.input_text) + self.caret.x
            x = self.text_object.font.get_rendered_size(self.input_text[0:index])[0]
            start_pos = self.text_object.position.x + x, self.text_object.position.y
            end_pos = self.text_object.position.x + x, self.text_object.position.y + self.caret.size.y
            pygame.draw.aaline(surface, self.fg_color, start_pos, end_pos)