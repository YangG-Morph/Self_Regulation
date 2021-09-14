
import pygame
from data.ui.panel import Panel


class PanelManager:
    def __init__(self, screen=None, database=None):
        self.panels = []  # TODO dictionary and set z_index?
        self.screen = screen
        self.component_clicked = False
        self.database = database

    def _adding(self, panel):
        if isinstance(panel, Panel):
            #panel.database = self.database  # TODO Find a better way, too much passing around
            self.panels.append(panel)
        else:
            raise TypeError(f"{panel} is not a Panel object. I only manage panels.")

    def add(self, *panels):
        if isinstance(panels, (list, tuple)):
            for panel in panels:
                self._adding(panel)
        else:
            #print("Setting database 2")
            self._adding(*panels)

    def update_position(self, window_size):
        [panel.update_position(window_size) for panel in self.panels]

    def handle_key_press(self, event):
        [panel.handle_key_press(event) for panel in self.panels]

    def handle_mouse(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN]:
            [panel.reset_components() for panel in self.panels]
        elif event.type in [pygame.MOUSEBUTTONUP]:
            #print("setting all to false")  # TODO NOW need to look for nested panels
            for panel in self.panels:  # TODO Finda better way, recursion?
                for component in panel.components:
                    if isinstance(component, Panel):
                        #print("Component is: ", component)
                        component.component_clicked = False
                panel.component_clicked = False
            #[setattr(panel, "component_clicked", False) for panel in self.panels]

    def update(self, delta_time):
        panels_copy = self.panels.copy()
        panels_copy.reverse()
        self.component_clicked = True if [panel for panel in panels_copy if panel.component_clicked is True] else False
        if self.component_clicked:  # TODO only highlight one when dragging mouse over
            for panel in self.panels:  # TODO Finda better way, recursion?
                for component in panel.components:
                    if isinstance(component, Panel):
                        #print("Component is: ", component)
                        component.component_clicked = True
                panel.component_clicked = True
            #[setattr(panel, "component_clicked", True) for panel in self.panels]  # TODO NOW need to look for nested panels

        [panel.update(delta_time) for panel in panels_copy]

    def draw(self):
        [panel.draw(self.screen) for panel in self.panels]


