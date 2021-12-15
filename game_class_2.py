import pygame
import random
import os
import random

font_name = pygame.font.match_font('arial')
def draw_text(text, size, x, y, mode = "midtop"):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    if mode == "midtop":
        text_rect.midtop = (x, y)
    elif mode == "topleft":
        text_rect.topleft = (x, y)
    elif mode == "center":
        text_rect.center = (x, y)
    return text_surface, text_rect


class InputBox:
    COLOR_INACTIVE = (0, 0, 0)
    COLOR_ACTIVE = (255, 0, 0)
    def __init__(self, x, y, w, h, text='', font_name = pygame.font.match_font('arial')):
        self.FONT = pygame.font.Font(font_name, 15)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.w = w
        self.h = h
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.visible =True

    