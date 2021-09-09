import pygame
import sys
from pygame import Color, Vector2
from data.constants import GAME_SIZE, FPS
from data.assets.paths import BG
from data.ui.panel import Panel
from data.ui.text_button import TextButton
from data.database import Database
from data.panel_manager import PanelManager
from data.ui.text_input import TextInput
from data.ui.text_label import TextLabel
from data.ui.alarm import Alarm


class App:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.clock = pygame.time.Clock()
        self.database = Database()
        self.panel_manager = PanelManager(screen)

        self.bg_color = Color("black")
        self.fg_color = Color("white")
        self.bg_image = pygame.transform.smoothscale(BG, GAME_SIZE).convert_alpha()

        self.back_panel = Panel(size=GAME_SIZE, bg_color=Color(0, 0, 0, 0).lerp((0, 0, 0), 0.5),
                                fg_color=pygame.Color("red"), background_image=self.bg_image)

        self.top_panel = Panel(size=(GAME_SIZE[0], 200), bg_color=Color(50, 50, 50, 0).lerp((0, 0, 0), 0.5),
                               fg_color=pygame.Color("white"), margin=30)

        self.bottom_panel = Panel(size=(GAME_SIZE[0], GAME_SIZE[0] - 750),
                                  bg_color=Color(50, 50, 50, 100).lerp((0, 0, 0), 0.5),
                                  fg_color=Color("lightblue").lerp((0, 0, 0), 0.2),
                                  margin=30, margin_top=150,
                                  )
        self.bottom_left_panel = Panel(size=(GAME_SIZE[0] / 2, GAME_SIZE[1]),
                                       bg_color=Color(50, 50, 50, 100).lerp((0, 0, 0), 0.5),
                                       fg_color=Color("lightblue").lerp((0, 0, 0), 0.2),
                                       database=self.database)

        self.bottom_right_panel = Panel(size=(GAME_SIZE[0] / 3, GAME_SIZE[0] - 750),
                                        bg_color=Color(50, 50, 50, 100).lerp((0, 0, 0), 0.5),
                                        fg_color=Color("lightblue").lerp((0, 0, 0), 0.2),
                                        margin_left=GAME_SIZE[0] / 2,

                                        # Position determined by id
                                        )

        self.text_label = TextLabel(text="Tasks:", font_size=40,
                                    bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                                    fg_color=Color("white"),
                                    )
        self.text_input = TextInput(size=(100, 50),
                                    position=(0, 0),
                                    bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                                    fg_color=Color("white"),
                                    align_left=True,
                                    r=5,
                                    margin_left=160,
                                    enter_press_action=lambda text, create_type: self._create_entry(text=text,
                                                                                                    create_type=create_type),
                                    )

        self.alarm = Alarm(size=(10, 100),
                           bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                           fg_color=Color("grey"),
                           )

        self.panel_manager.add(self.back_panel, self.top_panel, self.bottom_panel)
        self.panel_manager.update_position(Vector2(pygame.display.get_surface().get_size()))
        self.bottom_panel.add(self.bottom_left_panel, self.bottom_right_panel)
        self.top_panel.add(self.text_label, self.text_input)
        self.bottom_right_panel.add(self.alarm)

        self._load_tasks()

    def _load_tasks(self):
        for task in self.database.get_tasks():
            self._create_entry(task[1])

    def _create_entry(self, text="Text shows up here", create_type="loading"):
        new_entry = TextButton(text=text,
                               size=(100, 50),
                               position=(0, 0),
                               bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                               fg_color=Color("white"),
                               align_left=True,
                               r=5,
                               )
        self.bottom_left_panel.add(new_entry, create_type=create_type)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # or event.type in [pygame.KEYDOWN] and event.key in [pygame.K_ESCAPE]:
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

            self.panel_manager.update()
            self.panel_manager.draw()

            self.clock.tick(FPS)
            pygame.display.flip()
