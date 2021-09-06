from pygame import Vector2
from data.ui.font import Font
from data.ui.base import Base


class Text(Base):
    def __init__(self,
                 text="None",
                 font_size=24,
                 *args, **kwargs
                 ):
        super().__init__(*args,**kwargs)
        self.text = text
        self.font = Font()
        self.font.set_size(font_size)
        self.rendered_text = self.font.render(self.text, self.fg_color)
        self.size = Vector2(self.rendered_text.get_size())

    def _update_text(self):
        self.size = Vector2(self.font.get_rendered_size(self.text))
        self.rendered_text = self.font.render(self.text, self.fg_color)

    def update_position(self, pos):
        self.position.xy = pos

    def draw(self, surface):
        surface.blit(self.rendered_text, self.position.xy)

    def set_font_size(self, text_size):
        self.font.set_size(text_size)
        self._update_text()

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self._update_text()

    def get_width(self):
        return self.rendered_text.get_width()

    def get_height(self):
        return self.rendered_text.get_height()
