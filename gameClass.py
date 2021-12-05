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
        self.viseble = True
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
        if not self.viseble:
            return
        self.surf.fill((169, 169, 169))
        rect = self.image.get_rect()
        rect.center = (self.width / 2, 3 * self.height / 4 )
        self.surf.blit(self.image, rect)
        if self.on:
            self.surf.blit(self.text_surface2, self.text_rect2)
        screen.blit(self.surf, self.rect)
        screen.blit(self.text_surface1, self.text_rect1)

class PlayerSprites(pygame.sprite.Sprite):
    def __init__(self, playerImage = None, nickname = '', width = 100, height = 100, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.text_size = 20
        self.playerImage = pygame.transform.scale(playerImage, (width, height - 2 * self.text_size))
        self.playerImageRect = self.playerImage.get_rect()
        self.playerImageRect.midtop = (width / 2, 0)
        self.nickname = nickname
        self.text_surface1, self.text_rect1 = draw_text(nickname, self.text_size , width / 2, self.height - 2 * self.text_size)
        self.text_surface2, self.text_rect2 = draw_text("Score: 0", self.text_size, width / 2, self.height - self.text_size)
        self.value = 0
        self.viseble = True
    @property
    def score(self):
        return self.value

    @score.setter
    def score(self, x):
        self.value = x
        (self.text_surface2, self.text_rect2) = draw_text("Score: " + str(x), 15, self.width / 2, self.height - 15)
    @property
    def name(self):
        return self.nickname;

    @name.setter
    def name(self, x):
        self.nickname = x
        (self.text_surface1, self.text_rect1) = draw_text(x, self.text_size , self.width / 2, self.height - 2 * self.text_size)
   
    def update(self):
        self.surf.fill((255,255,255))
        self.surf.blit(self.playerImage, self.playerImageRect)
        self.surf.blit(self.text_surface1, self.text_rect1)
        self.surf.blit(self.text_surface2, self.text_rect2)
        
    def draw(self, screen):
        if not self.viseble:
            return
        screen.blit(self.surf, self.rect)

class Button(pygame.sprite.Sprite):
    button_normal_back_color = (169, 169, 169);
    button_hover_back_color = (169, 169, 169);
    button_pressed_back_color = (255, 255, 0);
    def __init__(self, x, y, Width, Height, text, on_click=lambda x: None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x;
        self.y = y;
        self.height = Height;
        self.width = Width;
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.state = 'normal'
        self.on_click = on_click
        self.text = draw_text(text, Height // 3, Width / 2, Height / 2, "center")
        self.viseble = True
        
    def update(self):
        pass

    def draw(self, screen):
        if not self.viseble:
            return
        self.surf.fill(self.back_color)
        self.surf.blit(self.text[0], self.text[1])
        screen.blit(self.surf, self.rect)

    def handle_mouse_event(self, type, pos):
        if not self.viseble:
            return
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
        self.w = w
        self.h = h
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.viseble =True

    def handle_event(self, event):
        if not self.viseble:
            return
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
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        pass

    def draw(self, screen):
        if not self.viseble:
            return
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+self.w // 2, self.rect.y+self.h // 3))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class RoundIter():
    def __init__(self, cnt = 1):
        self.filePath = os.path.join(os.path.dirname(__file__), 'video')
        self.videoPath = []
        random.seed()
        for i in range(cnt):
            numRound =  random.randint(1, 3)
            video, timeCode = os.path.join(self.filePath, "round" + str(numRound) + '.mov'), os.path.join(self.filePath, "round" + str(numRound) + '.txt')
            while (video, timeCode) in self.videoPath:
                numRound =  random.randint(1, cnt)
                video, timeCode = os.path.join(self.filePath, "round" + str(numRound) + '.mov'), os.path.join(self.filePath, "round" + str(numRound) + '.txt')
            self.videoPath.append((video, timeCode))
        self._start = 0
        self._end = cnt  -1

    def __iter__(self):
        return self

    def __next__(self):
        if self._start > self._end:
            raise StopIteration()
        tmp = self._start
        self._start = tmp + 1
        time = open(self.videoPath[tmp][1], 'r').read().split('|')
        timecode = []
        for t in time:
            t = t.split(':')
            mn = 1000
            ans = 0
            for el in t[::-1]:
                ans += int(el) * mn
                mn *= 60
            timecode.append(ans)
        return (self.videoPath[tmp][0], timecode)

class CleverSurf(pygame.sprite.Sprite):
    def __init__(self, surf = None, rect = None, x = None, y = None):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.rect = rect
        self.viseble = True
        self.pos = (x, y)
    
    @property
    def surf(self):
        return self.s;

    @surf.setter
    def surf(self, x):
        self.s = x
    
    @property
    def rect(self):
        return self.r;
    
    @rect.setter
    def rect(self, x):
        self.r = x
    
    @property
    def pos(self):
        return self.p;
    
    @pos.setter
    def pos(self, pos):
        self.p = pos
        if (pos != (None, None)):
            self.rect.center = pos

    @property
    def size(self):
        return self.si;
    
    @size.setter
    def size(self, size):
        self.si = size
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect()
    
    def update(self):
        pass

    def draw(self, screen):
        if not self.viseble:
            return
        screen.blit(self.surf, self.rect)

        