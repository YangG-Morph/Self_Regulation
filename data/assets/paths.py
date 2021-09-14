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

ASSETS_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = get_parent_dir(ASSETS_DIR)
DEBUG_DIR = os.path.join(DATA_DIR, "debug")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

""" FONT """
QUICKSAND_LIGHT = font_path("Quicksand-Light.otf")
QUICKSAND_BOLD = font_path("Quicksand-Bold.otf")


""" IMAGES """
BG = pygame.image.load(image_path("bg.jpg")).convert_alpha()

#debug_filename = "debug.txt"
#with open('debug_filename', 'w') as f:
#    f.write(f"{QUICKSAND_LIGHT}\n"
#            f"{QUICKSAND_BOLD}")
