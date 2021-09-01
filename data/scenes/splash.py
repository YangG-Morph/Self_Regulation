import pygame
from data.scenes.scene import Scene
from data.ui.text import Text



class Splash(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.text = Text(text="Welcome,       to Self Regulation.", center_x=True, center_y=True)
        self.text_load = Text(text="Loading...", position=self.text.position+(0, 50))
        self.bg_color = pygame.Color("black")
        self.fg_color = pygame.Color("white")
        self.text.set_size(34)
        self.timer = 5
        self.prev_timer = self.timer
        self.is_loading = False
        self.text.update_position(pygame.display.get_surface().get_size())

    def draw_background(self):
        self.game.screen.fill(self.bg_color)

    def draw_foreground(self):
        self.text.draw(self.game.screen)
        if self.is_loading:
            self.text_load.draw(self.game.screen)

    def handle_time(self, dt):
        self.prev_timer = self.timer
        self.timer -= dt

        if self.timer <= 0:
            self.game.scene_manager.next_scene()
        elif self.timer <= 3:
            self.is_loading = True