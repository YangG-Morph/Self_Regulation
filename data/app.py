import pygame
import sys
from pygame import Color, Vector2
from data.constants import GAME_SIZE, FPS, MUSIC_END, SOUND_END
from data.assets.paths import BG, BG_MUSIC
from data.ui.panel import Panel
from data.ui.text_button import TextButton
from data.database import Database
from data.panel_manager import PanelManager
from data.ui.text_input import TextInput
from data.ui.text_label import TextLabel
from data.ui.button import Button
from data.ui.alarm import Alarm
from data.music_player import MusicPlayer
from data.sound_player import SoundPlayer


class App:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.clock = pygame.time.Clock()
        self.database = Database()
        self.panel_manager = PanelManager(screen)
        self.music_player = MusicPlayer()
        # self.sound_player = SoundPlayer()

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
                                    margin_left=30,
                                    margin_top=30,
                                    resizable=True,
                                    )
        self.text_input = TextInput(size=(100, 50),
                                    position=(0, 0),
                                    bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                                    fg_color=Color("white"),
                                    align_left=True,
                                    r=5,
                                    margin_left=160,
                                    margin_top=30,
                                    resizable=True,
                                    enter_press_action=lambda text, create_type: self._create_entry(text=text,
                                                                                                    create_type=create_type),
                                    )

        self.alarm = Alarm(size=(250, 250),
                           bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                           fg_color=Color("grey"),
                           margin_left=300,
                           margin_top=300,
                           resizable=False,
                           )

        self.play_music_button = TextButton(text="Play music",
                                            size=(130, 30),
                                            bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                                            fg_color=Color("white"),
                                            margin_left=-30,
                                            margin_top=-30,
                                            resizable=False,
                                            )
        self.play_music_button.text_object.set_font_size(20)
        self.play_music_button.left_action = lambda: [self.music_player.play(),
                                                      self.play_music_button.text_object.set_text("Pause")
                                                      if self.play_music_button.text_object.text == "Play music"
                                                      else self.play_music_button.text_object.set_text("Play music")]
        self.next_music_button = TextButton(text="Next",
                                            size=(80, 30),
                                            bg_color=Color("lightblue").lerp((0, 0, 0), 0.5),
                                            fg_color=Color("white"),
                                            margin_left=-30+130,
                                            margin_top=-65,
                                            resizable=False,
                                            )
        self.next_music_button.text_object.set_font_size(20)
        self.next_music_button.left_action = lambda: [self.music_player.next(), self.play_music_button.text_object.set_text("Pause")]
        #self.play_music_button.right_action = lambda: [self.music_player.pause(), self.play_music_button.text_object.set_text("Play music")]

        self.panel_manager.add(self.back_panel, self.top_panel, self.bottom_panel)
        self.panel_manager.update_position(Vector2(pygame.display.get_surface().get_size()))
        self.bottom_panel.add(self.bottom_left_panel, self.bottom_right_panel)
        self.top_panel.add(self.play_music_button, self.next_music_button, self.text_label, self.text_input)
        self.bottom_right_panel.add(self.alarm)

        self._load_tasks()
        # self.music_player.play()

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
                               margin_left=30,
                               margin_top=30,
                               r=5,
                               resizable=True,
                               )
        new_entry.right_action = lambda: new_entry.delete_self()
        self.bottom_left_panel.add(new_entry, create_type=create_type)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                self._exit_app()
            elif event.type in [pygame.WINDOWRESIZED]:
                self.panel_manager.update_position(Vector2(pygame.display.get_surface().get_size()))
            elif event.type in [pygame.KEYDOWN]:
                self.panel_manager.handle_key_press(event)
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self.panel_manager.handle_mouse(event)
                self.alarm.handle_events(event)
            elif event.type in [MUSIC_END]:
                self.music_player.reset_pos()
                self.music_player.next()
            elif event.type in [SOUND_END]:
                self.alarm.sound_player.sound_end()

    def _exit_app(self):
        pygame.quit()
        sys.exit()

    def run(self):
        self._main_loop()

    def _main_loop(self):
        while True:
            delta_time = self.clock.tick(FPS) / 1000
            self._handle_events()

            self.panel_manager.update(delta_time)
            self.panel_manager.draw()

            pygame.display.flip()
