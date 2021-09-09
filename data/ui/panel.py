import pygame.display
import pygame
from data.ui.base import Base
from data.constants import ALLOWED_KEYS
from data.ui.text_button import TextButton


class Panel(Base):
    def __init__(self, database=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.components = []
        self.component_clicked = False
        self.database = database

    def _adding(self, component, create_type):  # TODO don't put panels in panels
        component.id = max(0, min(len(self.components),
                                  len(self.components) + 1))  # TODO incorrect len since other panels inside
        #component.size.x = self.size.x / 2  # TODO remove?
        component.rebuild_surface()
        component.parent = self
        from data.ui.alarm import Alarm
        # component.margin += self.margin
        for attribute in ["margin_top", "margin_left", "margin_right", "margin_bottom"]:
            # if isinstance(component, Alarm):
            #    print(f"Parent {self} {attribute}: ", getattr(self, attribute))
            #    print(f"Alarm {attribute}: ", getattr(component, attribute))
            # if isinstance(component, Panel):
            #    print(f"Parent {self} {attribute}: ", getattr(self, attribute))
            #    print(f"Panel {attribute}: ", getattr(component, attribute))
            # print(f"Alarm top: ", getattr(component, "margin_top"))
            if getattr(self, attribute) != getattr(component, attribute) and getattr(component, attribute) == 0:
                setattr(component, attribute, getattr(self, attribute))
                # if isinstance(component, Alarm):
                #    print(f"Parent {self} {attribute}: ", getattr(self, attribute))
                #    print(f"Alarm {attribute}: ", getattr(component, attribute))
                # setattr(component, attribute, getattr(component, attribute) + getattr(self, attribute))
            else:
                setattr(component, attribute, getattr(component, attribute) + getattr(self, attribute))
                # setattr(self, attribute, self.margin)
                if not getattr(component, attribute):
                    setattr(component, attribute, 0)
        if self.database and create_type == "save":
            self.database.insert(component.id, component.text_object.text)
        self.components.append(component)

    def add(self, *elements, create_type=None):
        if isinstance(elements, (tuple, list)):
            for i, element in enumerate(elements):
                self._adding(element, create_type)
        else:
            self._adding(elements[0], create_type)
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
                #print("Deletion detected")
                was_deleting = True
                self.database.delete(component.id, component.text_object.text)
                self.components.remove(component)
                del component
        if was_deleting:
            #print("Was deleting and database: ", self.database)
            self.database.create_table("temp")
            for i, component in enumerate(self.components):
                component.id = i
                self.database.insert(component.id, component.text_object.text, "temp")
            self.database.delete_all()
            self.database.copy_from_temp()
            self.database.delete_all("temp")
            window_size = pygame.display.get_surface().get_size()
            [obj.update_position(window_size) for obj in self.components]
        [component.update() for component in self.components]

    def get_active_component(self):
        for component in self.components:
            if hasattr(component, "input_mode") and component.input_mode:  # TODO might work incorrectly if input_text is nested within panels
                return component
        return None

    def handle_key_press(self, event):
        component = self.get_active_component()
        if component and event.key in ALLOWED_KEYS:
            if event.key == pygame.K_BACKSPACE:  # TODO CTRL + BACKSPACE not working at the front of text
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
                        component.enter_press_action(component.text_object.text, create_type="save")
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
            elif event.key in [pygame.K_ESCAPE]:
                self.reset_components()
            else:
                component.input_text = component.input_text[
                                       :component.caret.x] + event.unicode + component.input_text[
                                                                             component.caret.x:]
                component.caret.x = len(component.input_text) if component.caret.x > len(
                    component.input_text) else component.caret.x + 1

    def update_position(self, window_size):
        self.size = pygame.Vector2(window_size)
        super().update_position(self.size)
        self.rebuild_surface()
        [component.update_position(self.size) for component in self.components]

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.surface, self.position.xy)
        # pygame.draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, 5)
        [obj.draw(surface) for obj in self.components]
