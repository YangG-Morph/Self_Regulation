import pygame
import os
from data.assets.paths import OPENDYSLEXIC_REGULAR, OPENDYSLEXIC_BOLD

class Font:
    def __init__(self):
        self.size = 24
        self._font = pygame.font.Font(OPENDYSLEXIC_REGULAR, self.size)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, new_font):
        pass

    def set_size(self, size):
        self.size = size
        self._font = pygame.font.Font(OPENDYSLEXIC_REGULAR, self.size)

    def get_font_size(self):
        return self.size

    def get_rendered_size(self, text):
        return self.font.size(text)

    def get_height(self):
        return self.font.get_height()

    def set_italic(self, is_on):
        self.font.set_italic(is_on)

    def set_bold(self, is_on):
        if is_on:
            self.font = pygame.font.Font(OPENDYSLEXIC_BOLD, self.size)
        else:
            self.font = pygame.font.Font(OPENDYSLEXIC_REGULAR, self.size)

    def render(self, text, color):
        return self.font.render(text, True, color)
