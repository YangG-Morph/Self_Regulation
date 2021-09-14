
import pygame
from data.constants import GAME_SIZE, CAPTION

def main():
    pygame.init()
    screen = pygame.display.set_mode(GAME_SIZE, flags=pygame.HIDDEN)
    pygame.display.set_caption(CAPTION)

    pygame.key.set_repeat(500, 50)

    from data.app import App
    app = App(screen)
    pygame.display.set_mode(GAME_SIZE, flags=pygame.RESIZABLE)
    app.run()

if __name__ == '__main__':
    main()