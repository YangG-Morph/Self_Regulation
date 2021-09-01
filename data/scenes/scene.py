import random
import sys
import pygame
from data.ui.text import Text

class Scene:
    def __init__(self, game):
        self.game = game
        #self.text = Text(text=f"{self.__class__.__name__}")
        self.bg_color = pygame.Color("black")
        self.fg_color = pygame.Color("white")
        self.timer = 0
        self.prev_timer = self.timer

    def draw_background(self):
        pass

    def draw_foreground(self):
        pass

    def handle_exit(self, event):
        if event.type in [pygame.QUIT] or event.type in [pygame.KEYDOWN] and event.key in [pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    def handle_keys(self, event):
        if event.type in [pygame.KEYDOWN]:
            if event.key in [pygame.K_a]:
                self.game.scene_manager.previous_scene()
            if event.key in [pygame.K_d]:
                self.game.scene_manager.next_scene()

    def handle_time(self, dt):
        pass

    def handle_mouse(self, event):
        pass

    def handle_mouse_movement(self):
        pass

    def handle_sprite_events(self, event):
        pass

    def scene_enter(self):
        pass

    def scene_exit(self):
        pass

