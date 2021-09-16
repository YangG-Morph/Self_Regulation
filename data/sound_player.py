import os
import random
import pygame
from data.assets.paths import GET_READY_SOUND, COUNTDOWN_SOUND, FINISHED_SOUND


class SoundPlayer:
    def __init__(self):
        self._sound_cached = {sound.rpartition(os.sep)[2].rpartition(".")[0]: pygame.mixer.Sound(sound) for sound in [GET_READY_SOUND, COUNTDOWN_SOUND, FINISHED_SOUND]}
        self.channel = pygame.mixer.Channel(5)
        self._last_sound = None

    def play(self, sound_name):
        self.channel.play(self._sound_cached.get(sound_name))

    def stop(self):
        self.channel.stop()

    def get_busy(self):
        if self.channel.get_busy():
            self._last_sound = self.channel.get_sound()
        return self.channel.get_busy()

    def sound_end(self):
        if self._last_sound == self._sound_cached.get("get_ready"):
            self.channel.play(self._sound_cached.get("3_2_1"))