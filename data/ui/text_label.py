


from data.ui.base import Base
from data.ui.text import Text

class TextLabel(Base):
    def __init__(self,text="Not implemented", font_size=24, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_object = Text(text=text, position=self.position, fg_color=self.fg_color)
        self.text_object.set_font_size(font_size)
        self.text_object.update_position(self.position.xy)

    def draw(self, surface):
        super().draw(surface)
        self.text_object.draw(surface)





