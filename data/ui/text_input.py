
import pygame
from data.ui.text import Text
from data.ui.base import Base
from data.ui.caret import Caret
from data.ui.text_button import TextButton

class TextInput(TextButton):
    def __init__(self,text="Not implemented", font_size=24, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = Text(text=text, position=self.position, fg_color=self.fg_color)
        self.text.set_font_size(font_size)
        self.text.update_position(self.position.xy)
        self.input_mode = False
        self.prev_text = text
        self.input_text = text
        self.original_text = text  # Store text when input started, restore when escape pressed
        self.caret = Caret(pygame.Vector2(1, self.text.size.y))
        self.is_pressed = False


