import random
import pygame
from data.assets.paths import BG_MUSIC

class MusicPlayer:
    def __init__(self):
        self.shuffled_music = BG_MUSIC
        random.shuffle(self.shuffled_music)
        self.music_cached = [lambda song=song: pygame.mixer.music.load(song) for song in self.shuffled_music]
        self.shuffled_music = (music for music in self.music_cached)
        self.next()

    def reset_songs(self):
        random.shuffle(self.music_cached)
        self.shuffled_music = (music for music in self.music_cached)

    def play(self):
        pass#pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        try:
            next(self.shuffled_music)()
        except StopIteration:
            self.stop()
            self.reset_songs()
        self.play()



