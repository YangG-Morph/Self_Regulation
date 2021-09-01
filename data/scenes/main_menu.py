from data.scenes.scene import Scene
import pygame
from data.ui.text import Text
from data.ui.button import Button
from data.ui.panel import Panel

class MainMenu(Scene):
    def __init__(self, game):
        super().__init__(game)
        #self.text = Text(text=str(self.__class__.__name__))
        self.bg_color = pygame.Color("black")
        self.fg_color = pygame.Color("white")
        self.button = Button(text="Hello world",
                             size=(120, 60),
                             position=(0,0),
                             bg_color=pygame.Color("lightblue"),
                             fg_color=pygame.Color("white"),
                             center_x=True,
                             center_y=True,
                             )
        self.panel = Panel(size=pygame.display.get_surface().get_size(), bg_color=pygame.Color("lightblue"))
        self.panel.add(self.button)
        self.panel.update_position(pygame.display.get_surface().get_size())

    def draw_background(self):
        self.game.screen.fill(self.bg_color)

    def draw_foreground(self):
        self.panel.draw(self.game.screen)

    def handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.button.pressed:
                print("clicked")

    #def handle_mouse_movement(self):
    #    if self.button.pressed:
    #        print("clicked")
