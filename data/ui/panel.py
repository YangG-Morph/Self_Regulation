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
                element.size.x = self.size.x / 2  # TODO remove?
                element.rebuild_surface()
                element.parent = self
                element.margin += self.margin
                element.margin_top += self.margin_top
                element.margin_left += self.margin_left
                element.margin_right += self.margin_right
                element.margin_bottom += self.margin_bottom
                self.components.append(element)
        else:
            elements[0].id = max(0, min(len(self.components), len(self.components) + 1))
            elements[0].size.x = self.size.x / 2  # TODO remove?
            elements[0].rebuild_surface()
            elements[0].parent = self
            elements[0].margin += self.margin
            elements[0].margin_top += self.margin_top
            elements[0].margin_left += self.margin_left
            elements[0].margin_right += self.margin_right
            elements[0].margin_bottom += self.margin_bottom
            self.components.append(elements[0])
        self.update_position(pygame.display.get_surface().get_size())

    def reset_components(self):
        for component in self.components:
            if hasattr(component, "input_mode") and component.input_mode:
                component.input_mode = False
                component.input_text = "Enter task here..."

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
                if hasattr(component, "enter_press_action"):
                    if component.text_object.text.strip():
                        component.enter_press_action(component.text_object.text)
                        component.set_text("")
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
        super().update_position(window_size)
        [obj.update_position(self.size) for obj in self.components]

    def draw(self, surface):
        super().draw(surface)
        if self.visible:
            surface.blit(self.surface, self.position.xy)
            #draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, 5)
            [obj.draw(surface) for obj in self.components]



