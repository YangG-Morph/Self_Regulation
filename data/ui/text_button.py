
import pygame
from data.ui.button import Button
from data.ui.text import Text
from data.ui.caret import Caret

class TextButton(Button):
    def __init__(self,text="Not implemented", font_size=24, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_object = Text(text=text, position=self.position, fg_color=self.fg_color)
        self.text_object.set_font_size(font_size)
        self.text_object.update_position(self.position.xy)
        self.input_mode = False
        self.prev_text = text
        self.input_text = text
        self.original_text = text  # TODO Store text_object when input started, restore when escape pressed
        self.caret = Caret(pygame.Vector2(1, self.text_object.size.y))
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

    def update(self, manager=None):
        if self.position.xy != self.rect.topleft or self.size.xy != self.rect.size:
            self.rect.update(self.position.xy, self.rect.size)

        if hasattr(manager, "component_clicked"):
            if manager.component_clicked:
                pass #print("manager: ", manager.component_clicked)
            if self.left_click and not manager.component_clicked:
                manager.component_clicked = True  # TODO Not being set to True, by value and not reference?
                #self.input_mode = True
                #self.caret.x = len(self.input_text)
                self.left_action()
            elif self.right_click and not manager.component_clicked:
                manager.component_clicked = True
                self.set_for_delete = True

        if self.prev_text != self.input_text:
            self.prev_text = self.input_text
            self.text_object.set_text(self.input_text)
        self.position.y = (self.size.y + self.padding) * self.id + self.margin_top
        #self.text_object.position.xy = (self.position.x + self.size.x / 2) - self.text_object.size.x / 2, \ # TODO Infinite feedback loop
        #                        (self.position.y + self.size.y / 2) - self.text_object.size.y / 2

    def left_action(self):
        pass  # print("Doing action")

    def draw(self, surface):
        super().draw(surface)
        self.text_object.draw(surface)
        #if self.input_mode:
        #    index = self.caret.x#len(self.input_text) + self.caret.x
        #    x = self.text_object.font.get_rendered_size(self.input_text[0:index])[0]
        #    start_pos = self.text_object.position.x + x, self.text_object.position.y
        #    end_pos = self.text_object.position.x + x, self.text_object.position.y + self.caret.size.y
        #    pygame.draw.aaline(surface, self.fg_color, start_pos, end_pos)