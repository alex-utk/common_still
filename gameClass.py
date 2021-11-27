import pygame
import random
import os

def draw_text(text, size, x, y, mode = 0, font_name = pygame.font.match_font('arial')):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    if mode == 0:
        text_rect.midtop = (x, y)
    else:
        text_rect.topleft = (x, y)
    return(text_surface, text_rect)

class timerSprite(pygame.sprite.Sprite):
    def __init__(self, fps = 30):
        pygame.sprite.Sprite.__init__(self)
        self.tick = 0
        self.fps = fps
        self.width = 100
        self.height = 100
        self.color = (0, 255, 0)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.spritesGroup = None
        self.interval = 0

    def timerStart(self, interval, spritesGroup, Width, Height, x, y):
        self.image = pygame.Surface((Width, Height))
        self.width = Width
        self.height = Height
        self.spritesGroup = spritesGroup
        self.interval = interval
        self.rect.center = (x, y)
        self.spritesGroup.add(self)
    
    def update(self):
        cntTick = self.fps * self.interval
        self.tick += 1
        scale = self.width * ( (cntTick - self.tick) / cntTick)
        if scale > 1:
            self.image = pygame.Surface((scale, 25))
            self.image.fill(self.color)
            txt = str(90 - self.tick // 30)
            size = self.height - 2
            (text_surface, text_rect) = draw_text(txt, size, 0, 0, 1)
            self.image.blit(text_surface, text_rect)
        else:
            self.spritesGroup.remove(self)

class PlayerSprites(pygame.sprite.Sprite):
    def __init__(self, playerImage, text, width = 100, height = 100, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.playerImage = pygame.transform.scale(playerImage, (width, height - 30))
        self.playerImageRect = self.playerImage.get_rect()
        self.playerImageRect.midtop = (width / 2, 0)
        (self.text_surface1, self.text_rect1) = draw_text(text, 15, width / 2, self.height - 30)
        (self.text_surface2, self.text_rect2) = draw_text("Score: 0", 15, width / 2, self.height - 15)
        self.value = 0
    @property
    def score(self):
        return self.value
    @score.setter
    def score(self, x):
        self.value = x
        (self.text_surface2, self.text_rect2) = draw_text("Score: " + str(x), 15, self.width / 2, self.height - 15)
    def draw(self, screen):
        self.surf.fill((255,255,255))
        self.surf.blit(self.playerImage, self.playerImageRect)
        self.surf.blit(self.text_surface1, self.text_rect1)
        self.surf.blit(self.text_surface2, self.text_rect2)
        screen.blit(self.surf, self.rect)

class Button(pygame.sprite.Sprite):
    button_normal_back_color = (169, 169, 169);
    button_hover_back_color = (169, 169, 169);
    button_pressed_back_color = (255, 255, 0);
    def __init__(self, x, y, w, h, text, on_click=lambda x: None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x;
        self.y = y;
        self.height = h;
        self.width = w;
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.state = 'normal'
        self.on_click = on_click
        self.text = draw_text(text, 15, w / 2, y / 2, 1)
        

    def draw(self, screen):
        self.surf.fill(self.back_color)
        self.surf.blit(self.text[0], self.text[1])
        screen.blit(self.surf, self.rect)

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.rect.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'
    @property
    def back_color(self):
        return dict(normal= self.button_normal_back_color,
                    hover= self.button_hover_back_color,
                    pressed= self.button_pressed_back_color)[self.state]

class InputBox:
    COLOR_INACTIVE = (0, 0, 0)
    COLOR_ACTIVE = (255, 0, 0)
    def __init__(self, x, y, w, h, text='', font_name = pygame.font.match_font('arial')):
        self.FONT = pygame.font.Font(font_name, 15)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

