import random
import sys
import pygame


class Scene:
    def __init__(self, game):
        self.game = game

        self.bg_color = pygame.Color("black")
        self.fg_color = pygame.Color("white")

    def draw_background(self):
        self.game.screen.fill(self.bg_color)

    def draw_foreground(self):
        self.text.draw(self.game.screen)

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

    def handle_mouse(self, event):
        pass

    def handle_sprite_events(self, event):
        pass

    def scene_enter(self):
        self.rand_color = random.SystemRandom().sample(range(0, 180), 3)

    def scene_exit(self):
        pass

