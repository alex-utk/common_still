import pygame

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False    #Статусы Игра работает\Игра запущена
        self.DISPLAY_W, self.DISPLAY_H = 720, 480   #Размеры окна width и height
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), flags = pygame.NOFRAME)
        self.font_name = '8-BIT WONDER.TTF'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

    def game_loop(self):
        """
        Запуск основного игрового цикла
        """
        while self.playing:
            self.check_events()
            if self.EXIT_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text('COCK AND BALL TORTURE', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()  

    def check_events(self):
        """
        Проверка событий совершенных игроком
        """
        self.reset_keys()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.EXIT_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        """
        Сброс статуса нажатия клавиш достпуных для использования пользователю
        """
        self.EXIT_KEY, self.BACK_KEY, self.UP_KEY, self.DOWN_KEY = False, False, False, False
    
    def draw_text(self, text, size, x, y):
        """
        Отрисовка текста для проверки работы игрового окна
        """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def get_size(self):
        """
        Получить размеры игрового окна
        """
        return self.DISPLAY_W, self.DISPLAY_H