
import pygame


class SceneManager:
    def __init__(self, scenes=None):
        self.scenes = scenes if scenes else {}
        self.max_index = len(self.scenes) - 1
        self.current_scene = list(self.scenes.keys())[0]
        self._previous_scene = None

    def draw_background(self):
        self.scenes.get(self.current_scene).draw_background()

    def draw_foreground(self):
        self.scenes.get(self.current_scene).draw_foreground()

    def handle_events(self):
        for event in pygame.event.get():
            self.scenes.get(self.current_scene).handle_exit(event)
            self.scenes.get(self.current_scene).handle_keys(event)
            self.scenes.get(self.current_scene).handle_mouse(event)
        self.scenes.get(self.current_scene).handle_mouse_movement()

    def handle_time(self, dt):
        self.scenes.get(self.current_scene).handle_time(dt)

    def current_index(self):
        return list(self.scenes.values()).index(self.scenes.get(self.current_scene))

    def get_index(self, key):
        if key in self.scenes.keys():
            index = list(self.scenes.keys()).index(key)
            return index
        else:
            raise IndexError(f"\"{key}\" does not exist in the scenes list")

    def next_scene(self, key=None):
        if type(key) == str:
            key = self.get_index(key)
        index = self.current_index()

        if index < self.max_index:
            self.scenes.get(self.current_scene).scene_exit()
            if key is not None:
                self.current_scene = list(self.scenes.keys())[key]
            else:
                self.current_scene = list(self.scenes.keys())[index + 1]
            self.scenes.get(self.current_scene).scene_enter()
            self._previous_scene = index

    def previous_scene(self):
        index = self.current_index()
        if index > 0:
            self.scenes.get(self.current_scene).scene_exit()
            if self._previous_scene is not None:
                self.current_scene = list(self.scenes.keys())[self._previous_scene]
            else:
                self.current_scene = list(self.scenes.keys())[index - 1]
            self.scenes.get(self.current_scene).scene_enter()
            self._previous_scene = index










