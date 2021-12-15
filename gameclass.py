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
    
class timerSprite(pygame.sprite.Sprite):
    def __init__(self, Width = 100, Height = 100, x = 0, y = 0, fps = 30, on_stop = lambda x: None, text = ""):
        pygame.sprite.Sprite.__init__(self)
        self.tick = 0
        self.fps = fps
        self.image = pygame.Surface((Width - 100, 25))
        self.surf = pygame.Surface((Width, Height))
        self.surf.fill((169, 169, 169))
        self.rect = self.surf.get_rect()
        self.width = Width
        self.height = Height
        self.on = False
        self.color = (0, 255, 0)
        self.image.fill(self.color)
        self.visible = True
        self.x = x
        self.y = y 
        self.rect.center = (x, y)
        self.interval = 0
        self.on_stop = on_stop
        (self.text_surface1, self.text_rect1) = draw_text(text, 50, self.x, self.y - Height / 4, "center")

    def timerStart(self, interval, on_stop = lambda x: None):
        self.interval = interval
        self.on = True
        self.tick = 0
        self.on_stop = on_stop
    
    def update(self):
        if not self.on:
            return
        cntTick = self.fps * self.interval
        self.tick += 1
        scale = (self.width - 100) * ( (cntTick - self.tick) / cntTick)
        if scale > 1:
            self.image = pygame.Surface((scale, 25))
            self.image.fill(self.color)
            txt = str(self.interval - self.tick // self.fps)
            (self.text_surface2, self.text_rect2) = draw_text(txt, 24, self.width / 2, 3 * self.height / 4, "center")
        else:
            self.on = False
            self.on_stop(self)

    def draw(self, screen):
        if not self.visible:
            return
        self.surf.fill((169, 169, 169))
        rect = self.image.get_rect()
        rect.center = (self.width / 2, 3 * self.height / 4 )
        self.surf.blit(self.image, rect)
        if self.on:
            self.surf.blit(self.text_surface2, self.text_rect2)
        screen.blit(self.surf, self.rect)
        screen.blit(self.text_surface1, self.text_rect1)

