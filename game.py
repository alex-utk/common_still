import pygame

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPALY_H = 720, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_W))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_W))
        self.font_name = '8-BIT WONDER.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)