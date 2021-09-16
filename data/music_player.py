import random
import pygame
from data.assets.paths import BG_MUSIC

class MusicPlayer:
    def __init__(self):
        self.shuffled_music = BG_MUSIC
        random.shuffle(self.shuffled_music)
        self.music_cached = [lambda song=song: pygame.mixer.music.load(song) for song in self.shuffled_music]
        self.shuffled_music = (music for music in self.music_cached)
        self.last_pos = 0
        self.next_pos = 0

    def reset_songs(self):
        random.shuffle(self.music_cached)
        self.shuffled_music = (music for music in self.music_cached)

    def reset_pos(self):
        self.last_pos = 0
        self.next_pos = 0

    def play(self):
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(0, self.last_pos)
            else:
                self.pause()
        except pygame.error as e:
            if str(e) == "music not loaded":
                self.next()
            else:
                raise e

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        self.next_pos = pygame.mixer.music.get_pos() / 1000.0
        self.last_pos += self.next_pos
        pygame.mixer.music.pause()

    def next(self):
        try:
            next(self.shuffled_music)()
        except StopIteration:
            self.stop()
            self.reset_songs()
        self.play()



