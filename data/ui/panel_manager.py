
import pygame
from data.ui.panel import Panel


class PanelManager:
    def __init__(self):
        self.panels = []

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
        [panel.update_position(window_size) for panel in self.panels]

    def handle_key_press(self, event):
        [panel.handle_key_press(event) for panel in self.panels]

    def handle_mouse(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN]:
            [panel.reset_components() for panel in self.panels]
        elif event.type in [pygame.MOUSEBUTTONUP]:
            [setattr(panel, "component_clicked", False) for panel in self.panels]

    def update(self):
        [panel.update() for panel in self.panels]

    def draw(self, surface):
        [panel.draw(surface) for panel in self.panels]


