import pygame
from constants import *

class InputHandler:
    @staticmethod
    def get_pressed_key(event):
        if event.type == pygame.KEYDOWN:
            key = event.unicode.lower()
            if key in KEY_MAPPING.values():
                return key
        return None
