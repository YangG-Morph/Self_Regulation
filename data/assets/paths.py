import os
import sys
import pygame


def real_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, os.path.join(ASSETS_DIR, relative_path))
    return os.path.join(ASSETS_DIR, relative_path)

def get_parent_dir(path, directories=1):
    path_result = None
    for i in range(directories):
        path_result = get_parent_dir(path.rpartition(os.sep)[0], i)
    return path_result or path

def font_path(filename):
    return real_path(os.path.join("fonts", filename))

def image_path(filename):
    return real_path(os.path.join("images", filename))

def music_path(filename):
    return real_path(os.path.join("music", filename))

def sound_path(filename):
    return real_path(os.path.join("sound", filename))

ASSETS_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = get_parent_dir(ASSETS_DIR)
DEBUG_DIR = os.path.join(DATA_DIR, "debug")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")
SOUND_DIR = os.path.join(DATA_DIR, "sound")

""" FONT """
QUICKSAND_LIGHT = font_path("Quicksand-Light.otf")
QUICKSAND_BOLD = font_path("Quicksand-Bold.otf")


""" MUSIC """
BG_MUSIC = [music_path(music) for music in os.listdir(real_path(MUSIC_DIR))]
BG_MUSIC.sort()


""" SOUND """
FEMALE = "karen"
GET_READY_SOUND = sound_path(os.path.join(FEMALE, "get_ready.wav"))
COUNTDOWN_SOUND = sound_path(os.path.join(FEMALE, "3_2_1.wav"))
FINISHED_SOUND = sound_path(os.path.join(FEMALE, "finished.wav"))

""" IMAGES """
BG = pygame.image.load(image_path("bg.jpg")).convert_alpha()

#debug_filename = "debug.txt"
#with open('debug_filename', 'w') as f:
#    f.write(f"{QUICKSAND_LIGHT}\n"
#            f"{QUICKSAND_BOLD}")
