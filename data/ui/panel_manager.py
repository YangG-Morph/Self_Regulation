
import pygame
from data.ui.panel import Panel


class PanelManager:
    def __init__(self, screen=None, task_function=None):
        self.panels = []  # TODO dictionary and set z_index?
        self.screen = screen
        self.component_clicked = False

    def add(self, *panels):
        if isinstance(panels, (list, tuple)):
            for panel in panels:
                if isinstance(panel, Panel):
                    self.panels.append(panel)
                else:
                    raise TypeError(f"{panel} is not a Panel object. I only manage panels.")
        else:
            if isinstance(panels, Panel):
                self.panels.append(panels)
            else:
                raise TypeError(f"{panels} is not a Panel object. I only manage panels.")

    def update_position(self, window_size):
        [panel.update_position(window_size) for panel in self.panels] # TODO working here

    def handle_key_press(self, event):
        [panel.handle_key_press(event) for panel in self.panels]

    def handle_mouse(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN]:
            [panel.reset_components() for panel in self.panels]
        elif event.type in [pygame.MOUSEBUTTONUP]:
            [setattr(panel, "component_clicked", False) for panel in self.panels]

    def update(self):
        panels_copy = self.panels.copy()
        panels_copy.reverse()

        self.component_clicked = True if [panel for panel in panels_copy if panel.component_clicked is True] else False
        if self.component_clicked:  # TODO only highlight one when dragging mouse over
            [setattr(panel, "component_clicked", True) for panel in self.panels]

        [panel.update(self) for panel in panels_copy]

        #self.component_clicked = True if [panel for panel in panels_copy if panel.component_clicked is True] else False
        #if self.component_clicked:  # TODO only highlight one when dragging mouse over
        #    [setattr(panel, "component_clicked", True) for panel in self.panels]

    def draw(self):
        [panel.draw(self.screen) for panel in self.panels]


