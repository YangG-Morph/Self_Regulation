import pygame
import sys
from pygame import Color, Vector2
from data.constants import GAME_SIZE, FPS, ALLOWED_KEYS
from data.assets.paths import BG
from data.ui.panel import Panel
from data.ui.text_button import TextButton
from data.ui.button import Button
from data.database import Database
from data.ui.panel_manager import PanelManager
from data.ui.text_input import TextInput
from data.ui.text import Text
from data.ui.text_label import TextLabel


class App:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.clock = pygame.time.Clock()
        self.panel_manager = PanelManager(screen)
        self.db = Database()
        self.db.connect()

        self.bg_color = Color("black")
        self.fg_color = Color("white")
        self.bg_image = pygame.transform.smoothscale(BG, GAME_SIZE).convert_alpha()

        self.back_panel = Panel(size=GAME_SIZE, bg_color=Color(50, 50, 50, 0).lerp((0, 0, 0), 0.5),
                                fg_color=pygame.Color("red"), background_image=self.bg_image, )

        self.top_panel = Panel(size=(GAME_SIZE[0], 200), bg_color=Color(50, 50, 50, 0).lerp((0, 0, 0), 0.5),
                               fg_color=pygame.Color("white"), margin=30)

        self.bottom_panel = Panel(size=(GAME_SIZE[0], 400),
                                  bg_color=Color(50, 50, 50, 100).lerp((0, 0, 0), 0.5),
                                  fg_color=Color("lightblue").lerp((0, 0, 0), 0.2),
                                  margin=30, margin_top=250,
                                  )
        self.text_task = TextLabel(text="Task:", size=(200, 200), position=(0, 0), font_size=50,
                                   bg_color=Color("lightblue").lerp((0, 0, 0), 0.5), fg_color=Color("white"),
                                   margin_left=0,
                                   )
        self.text_input = TextInput(text="Enter task here",
                                    size=(100, 100),
                                    position=(0, 0),
                                    bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                                    fg_color=Color("white"),
                                    align_left=True,
                                    r=5,
                                    margin_left=150,
                                    enter_press_action=lambda x: self._create_entry(x),
                                    )

        #self.add_entry_button = Button(size=(100, 100),
        #                               position=(800, 0),
        #                               bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
        #                               fg_color=Color("white"),
        #                               align_right=True,  # TODO
        #                               r=5,
        #                               )

        #self.add_entry_button.left_action = lambda: self._create_entry()
        self._create_entry()
        self.top_panel.add(self.text_task, self.text_input)#, self.add_entry_button)
        self.panel_manager.add(self.back_panel, self.top_panel, self.bottom_panel)
        self.panel_manager.update_position(Vector2(pygame.display.get_surface().get_size()))

    def _create_entry(self, text="Text shows up here"):
        new_entry = TextButton(text=text,
                               size=(100, 50),
                               position=(0, 0),
                               bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                               fg_color=Color("white"),
                               align_left=True,
                               r=5,
                               )
        self.bottom_panel.add(new_entry)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type in [pygame.QUIT] or event.type in [pygame.KEYDOWN] and event.key in [pygame.K_ESCAPE]:
                self._exit_app()
            elif event.type in [pygame.WINDOWRESIZED]:
                self.panel_manager.update_position(Vector2(pygame.display.get_surface().get_size()))
            elif event.type in [pygame.KEYDOWN]:
                self.panel_manager.handle_key_press(event)
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self.panel_manager.handle_mouse(event)

    def _exit_app(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self._main_loop()

    def _main_loop(self):
        while True:
            self._handle_events()

            # self.add_entry_button.update()
            self.panel_manager.update()
            self.panel_manager.draw()

            # self.add_entry_button.draw(self.screen)

            self.clock.tick(FPS)
            pygame.display.flip()
