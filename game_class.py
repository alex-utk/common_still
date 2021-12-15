import pygame
import random
import os
import random


font_name = pygame.font.match_font('arial')
def draw_text(text, size, x, y, mode = "midtop"):
    """
    Отрисовка текста
    """
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
        """ Спрайт таймера
        """
    def __init__(self, Width = 100, Height = 100, x = 0, y = 0, fps = 30, on_stop = lambda x: None, text = ""):
        pygame.sprite.Sprite.__init__(self)
        self.tick = 0
        self.fps = fps # кадры в секунду
        self.image = pygame.Surface((Width - 100, 25)) # изображение
        self.surf = pygame.Surface((Width, Height)) # поверхность
        self.surf.fill((169, 169, 169))
        self.rect = self.surf.get_rect() # прямоугольник
        self.width = Width # ширина
        self.height = Height # высота
        self.on = False # флаг включен
        self.color = (0, 255, 0) # цвет
        self.image.fill(self.color) 
        self.visible = True # видимость
        self.x = x # икс
        self.y = y # игрик
        self.rect.center = (x, y) # центр прямоугольника 
        self.interval = 0 # интервал
        self.on_stop = on_stop # остановка
        (self.text_surface1, self.text_rect1) = draw_text(text, 50, self.x, self.y - Height / 4, "center")

    def timerStart(self, interval, on_stop = lambda x: None):
        """
        Начало таймера
        """
        self.interval = interval
        self.on = True
        self.tick = 0
        self.on_stop = on_stop
    
    def update(self):
        """
        Обновление
        """
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
        """
        Отрисовка
        """
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

class PlayerSprites(pygame.sprite.Sprite):
    """ Класс спрайтов игроков
    """
    def __init__(self, playerImage = None, nickname = '', width = 100, height = 100, x = 0, y = 0):
        pygame.sprite.Sprite.__init__(self)
        self.width = width # ширина
        self.height = height # высота
        self.surf = pygame.Surface((self.width, self.height))# поверхность
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect() # прямоугольник
        self.rect.center = (x, y) # центр прямоугольника
        self.text_size = 20 # размер текста
        self.playerImage = pygame.transform.scale(playerImage, (width, height - 2 * self.text_size)) # Изображение игрока
        self.playerImageRect = self.playerImage.get_rect() #Прямоугольник изображения игрока
        self.playerImageRect.midtop = (width / 2, 0) # Координата изображения игрока
        self.nickname = nickname # Псевдоним
        self.text_surface1, self.text_rect1 = draw_text(nickname, self.text_size , width / 2, self.height - 2 * self.text_size)
        self.text_surface2, self.text_rect2 = draw_text("Score: 0", self.text_size, width / 2, self.height - self.text_size)
        self.value = 0 # Счёт
        self.visible = True # Видимость
    @property
    def score(self):
        """
        Счёт
        """
        return self.value

    @score.setter
    def score(self, x):
        """
        Счёт
        """
        self.value = x
        (self.text_surface2, self.text_rect2) = draw_text("Score: " + str(x), 15, self.width / 2, self.height - 15)
    @property
    def name(self):
        """
        Имя
        """
        return self.nickname;

    @name.setter
    def name(self, x):
        """
        Имя
        """
        self.nickname = x
        (self.text_surface1, self.text_rect1) = draw_text(x, self.text_size , self.width / 2, self.height - 2 * self.text_size)
   
    def update(self):
        """
        Обновление
        """
        self.surf.fill((255,255,255))
        self.surf.blit(self.playerImage, self.playerImageRect)
        self.surf.blit(self.text_surface1, self.text_rect1)
        self.surf.blit(self.text_surface2, self.text_rect2)
        
    def draw(self, screen):
        """
        Отрисовка
        """
        if not self.visible:
            return
        screen.blit(self.surf, self.rect)

class Button(pygame.sprite.Sprite):
    """ Класс кнопки
    """
    button_normal_back_color = (169, 169, 169);
    button_hover_back_color = (169, 169, 169);
    button_pressed_back_color = (255, 255, 0);
    def __init__(self, x, y, Width, Height, text, on_click=lambda x: None): 
        pygame.sprite.Sprite.__init__(self)
        self.x = x; # икс
        self.y = y; # игрик
        self.height = Height; # высота
        self.width = Width; # ширина
        self.surf = pygame.Surface((self.width, self.height)) # поверхность
        self.rect = self.surf.get_rect() # прямоугольник
        self.rect.center = (x, y) # центр прямоугольника
        self.state = 'normal' # состояние
        self.on_click = on_click # нажате
        self.text = draw_text(text, Height // 3, Width / 2, Height / 2, "center") # текст
        self.visible = True # Видимость
        
    def update(self):
        """
        Обновить объект
        """
        pass

    def draw(self, screen):
        """
        Отрисовка объекта
        """
        if not self.visible:
            return
        self.surf.fill(self.back_color)
        self.surf.blit(self.text[0], self.text[1])
        screen.blit(self.surf, self.rect)

    def handle_mouse_event(self, type, pos):
        """
        Событие для мыши
        """
        if not self.visible:
            return
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        """
        Движение мыши
        """
        if self.rect.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        """
        Нажатие мыши
        """
        if self.rect.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        """
        Отжим мыши
        """
        if self.state == 'pressed':
            self.on_click(self)
            self.state = 'hover'
    @property
    def back_color(self):
        """
        Цвет
        """
        return dict(normal= self.button_normal_back_color,
                    hover= self.button_hover_back_color,
                    pressed= self.button_pressed_back_color)[self.state]