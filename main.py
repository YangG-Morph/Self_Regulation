
import pygame
from data.constants import GAME_SIZE, CAPTION, MUSIC_END, SOUND_END

def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
    pygame.init()
    screen = pygame.display.set_mode(GAME_SIZE, flags=pygame.HIDDEN)
    pygame.display.set_caption(CAPTION)
    pygame.mixer.music.set_endevent(MUSIC_END)
    pygame.mixer.Channel(5).set_endevent(SOUND_END)

    pygame.key.set_repeat(500, 50)

    from data.app import App
    app = App(screen)
    pygame.display.set_mode(GAME_SIZE)
    app.run()

if __name__ == '__main__':
    main()