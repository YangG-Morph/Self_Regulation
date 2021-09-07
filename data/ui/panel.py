import pygame.display
import pygame
from data.ui.base import Base
from data.constants import ALLOWED_KEYS

class Panel(Base):
    def __init__(self, allow_database=None, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.components = []
        self.component_clicked = False
        self.database = None
        self.allow_database = allow_database

    def _adding(self, component, create_type):

        component.id = max(0, min(len(self.components), len(self.components) + 1))
        print("Counting: ", len(self.components), " and set id: ", component.id)
        component.size.x = self.size.x / 2  # TODO remove?
        component.rebuild_surface()
        component.parent = self
        component.margin += self.margin
        for attribute in ["margin_top", "margin_left", "margin_right", "margin_bottom"]:
            if getattr(self, attribute) != getattr(component, attribute):
                setattr(component, attribute, getattr(component, attribute) + getattr(self, attribute))
            else:
                setattr(self, attribute, self.margin)
                if not getattr(component, attribute):
                    setattr(component, attribute, 0)
        print("Why is id: ", component.id)
        if self.allow_database and create_type == "save":
            self.database.insert(component.id, component.text_object.text)
        self.components.append(component)

    def add(self, *elements, create_type):
        if isinstance(elements,(tuple, list)):
            for i, element in enumerate(elements):
                self._adding(element, create_type)
        else:
            self._adding(elements[0], create_type)
        print("Did get here?")
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
                print("Deleting: ", component.text_object.text, " with id: ", component.id)
                self.database.delete(component.id, component.text_object.text)
                self.components.remove(component)
                del component
        if was_deleting:
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
            if hasattr(component, "input_mode") and component.input_mode:
                return component
        return None

    def handle_key_press(self, event):
        component = self.get_active_component()
        if component and event.key in ALLOWED_KEYS:
            if event.key == pygame.K_BACKSPACE:  #TODO CTRL + BACKSPACE not working at the front of text
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
        super().update_position(window_size)
        self.size = pygame.Vector2(window_size)
        self.rebuild_surface()
        [obj.update_position(self.size) for obj in self.components]

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.surface, self.position.xy)
        #pygame.draw.rect(surface, self.fg_color, self.surface.get_rect(topleft=self.position.xy), 1, 5)
        [obj.draw(surface) for obj in self.components]



