import pygame.display
from pygame import Rect, Surface, draw
from data.ui.base import Base
from data.constants import ALLOWED_KEYS

class Panel(Base):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.components = []
        self.component_clicked = False

    def add(self, *elements):
        if isinstance(elements,(tuple, list)):
            for i, element in enumerate(elements):
                element.id = max(0, min(len(self.components), len(self.components) + 1))
                element.size.x = self.size.x / 2
                element.rebuild_surface()
                element.parent = self
                self.components.append(element)
        else:
            elements[0].id = max(0, min(len(self.components), len(self.components) + 1))
            elements[0].size.x = self.size.x / 2
            elements[0].rebuild_surface()
            elements[0].parent = self
            self.components.append(elements[0])
        self.update_position(pygame.display.get_surface().get_size())

    def reset_components(self):
        for component in self.components:
            if component.input_mode:
                component.input_mode = False

    def update(self):
        was_deleting = False
        for component in self.components:
            if component.set_for_delete:
                was_deleting = True
                self.components.remove(component)
                del component
        if was_deleting:
            for i, component in enumerate(self.components):
                component.id = i
            window_size = pygame.display.get_surface().get_size()
            [obj.update_position(window_size) for obj in self.components]
        [component.update() for component in self.components]

    def get_active_component(self):
        for component in self.components:
            if hasattr(component, "input_mode") and component.input_mode:
                return component
        return None

    def handle_key_press(self, event):
        component = self.get_active_component()
        if component and event.key in ALLOWED_KEYS:
            if event.key == pygame.K_BACKSPACE:
                if component.caret.x > 0:
                    if event.mod & pygame.KMOD_CTRL:
                        space = component.input_text.rfind(" ") + 1
                        if space == len(component.input_text):  # TODO Find a better way
                            space = component.input_text[:space].rfind(" ")
                        if space > -1:
                            component.input_text = component.input_text[:space]
                            component.caret.x = 0 if component.caret.x <= 0 else space
                    else:
                        component.input_text = component.input_text[
                                               :component.caret.x - 1] + component.input_text[
                                                                         component.caret.x:]
                        component.caret.x = 0 if component.caret.x <= 0 else component.caret.x - 1
            elif event.key == pygame.K_DELETE:
                if component.caret.x >= 0:
                    component.input_text = component.input_text[:component.caret.x] + component.input_text[
                                                                                      component.caret.x + 1:]
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                component.input_mode = False
            elif event.key in [pygame.K_UP]:
                component.caret.up()
            elif event.key in [pygame.K_DOWN]:
                component.caret.down()
            elif event.key in [pygame.K_LEFT]:
                component.caret.x = 0 if component.caret.x <= 0 else component.caret.x - 1
            elif event.key in [pygame.K_RIGHT]:
                component.caret.x = len(component.input_text) if component.caret.x > len(
                    component.input_text) else component.caret.x + 1
            elif event.key in [pygame.K_HOME]:
                component.caret.x = 0
            elif event.key in [pygame.K_END]:
                component.caret.x = len(component.input_text)
            else:
                component.input_text = component.input_text[
                                       :component.caret.x] + event.unicode + component.input_text[
                                                                             component.caret.x:]
                component.caret.x = len(component.input_text) if component.caret.x > len(
                    component.input_text) else component.caret.x + 1

    def update_position(self, window_size):
        self.size.xy = window_size
        if self.size.x >= window_size[0]:
            self.size.x = window_size[0] - self.margin
        if self.size.y >= window_size[1]:
            self.size.y = window_size[1] - self.margin
        self.surface = Surface(self.size.xy).convert_alpha()
        self.surface.fill(self.bg_color)
        self.position.x = self.margin / 2
        self.position.y = self.margin / 2
        if self.background_image:
            self.stretched_background_image = pygame.transform.smoothscale(self.background_image, window_size)
        [obj.update_position(window_size) for obj in self.components]

    def draw(self, surface):
        super().draw(surface)
        if self.visible:
            surface.blit(self.surface, self.position.xy)
            draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, 5)
            [obj.draw(surface) for obj in self.components]



