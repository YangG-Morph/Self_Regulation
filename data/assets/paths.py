import os
import sys

def real_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, os.path.join(ASSETS_DIR, relative_path))
    return os.path.join(ASSETS_DIR, relative_path)

def font_path(filename):
    return real_path(os.path.join("fonts", filename))

ASSETS_DIR = os.path.abspath(os.path.dirname(__file__))
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

""" FONT """
OPENDYSLEXIC_REGULAR = font_path("OpenDyslexic-Regular.otf")
OPENDYSLEXIC_BOLD = font_path("OpenDyslexic-Bold.otf")

with open('debug.txt', 'w') as f:
    f.write(f"{OPENDYSLEXIC_REGULAR}\n"
            f"{OPENDYSLEXIC_BOLD}")
