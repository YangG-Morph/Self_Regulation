import pygame
import sys
from pygame import RESIZABLE, DOUBLEBUF, HWSURFACE
from data.constants import SCREEN_SIZE, FPS
from data.scenes.SceneManager import SceneManager
from data.scenes.Splash import Splash
from data.scenes.MainMenu import MainMenu
from data.scenes.Settings import Settings
import time

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.clock = pygame.time.Clock()
        scenes = {"splash": Splash(self), "MainMenu": MainMenu(self), "Settings": Settings(self)}
        self.scene_manager = SceneManager(scenes)


    def run(self):
        while 1:
            self.scene_manager.draw_background()
            self.scene_manager.draw_foreground()
            self.scene_manager.handle_events()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    pygame.init()
    flags = RESIZABLE | DOUBLEBUF | HWSURFACE
    display = pygame.display.set_mode(SCREEN_SIZE, flags)
    pygame.display.set_caption("Particle Simulator")

    Game(display).run()


