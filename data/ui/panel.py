import pygame.display
import pygame
from data.ui.base import Base
from data.constants import ALLOWED_KEYS

class Panel(Base):
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.components = []
        self.component_clicked = False
        self._set_margins()


    def _set_margins(self):  # TODO margins not setting properly
        for attribute in ["margin_top", "margin_left", "margin_right", "margin_bottom"]:
            if self.margin > 0 and getattr(self, attribute) == 0:
                setattr(self, attribute, self.margin)

    def _adding(self, element):
        element.size.x = self.size.x / 2  # TODO remove?
        element.rebuild_surface()
        element.parent = self
        element.margin += self.margin
        for attribute in ["margin_top", "margin_left", "margin_right", "margin_bottom"]:
            if getattr(self, attribute) != getattr(element, attribute):
                setattr(element, attribute, getattr(element, attribute) + getattr(self, attribute))
            else:
                setattr(self, attribute, self.margin)
                if not getattr(element, attribute):
                    setattr(element, attribute, 0)

    def add(self, *elements):
        if isinstance(elements,(tuple, list)):
            for i, element in enumerate(elements):
                element.id = max(0, min(len(self.components), len(self.components) + 1))
                self._adding(element)
                self.components.append(element)
        else:
            elements[0].id = max(0, min(len(self.components), len(self.components) + 1))
            self._adding(elements[0])
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
        self.size = pygame.Vector2(window_size)
        self.rebuild_surface()
        [obj.update_position(self.size) for obj in self.components]

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.surface, self.position.xy)
        #pygame.draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, 5)
        [obj.draw(surface) for obj in self.components]



