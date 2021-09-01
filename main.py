import pygame
import sys
from pygame import RESIZABLE, DOUBLEBUF, HWSURFACE
from data.constants import SCREEN_SIZE, FPS, CAPTION
from data.scenes.scene_manager import SceneManager
from data.scenes.splash import Splash
from data.scenes.main_menu import MainMenu
from data.scenes.settings import Settings
import time

class Game:
    def __init__(self, screen):
        time.sleep(0.01)
        self.screen = screen
        self.screen.set_alpha(None)
        self.clock = pygame.time.Clock()
        scenes = {"splash": Splash(self), "MainMenu": MainMenu(self), "Settings": Settings(self)}
        self.scene_manager = SceneManager(scenes)

    def run(self):
        dt = 0
        while 1:
            self.scene_manager.draw_background()
            self.scene_manager.draw_foreground()
            self.scene_manager.handle_events()
            self.scene_manager.handle_time(dt)
            pygame.display.flip()
            dt = self.clock.tick(FPS) / 1000

if __name__ == '__main__':
    pygame.init()
    flags = RESIZABLE | DOUBLEBUF | HWSURFACE
    display = pygame.display.set_mode(SCREEN_SIZE, flags)
    pygame.display.set_caption(CAPTION)


    Game(display).run()


