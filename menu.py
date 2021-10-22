import pygame
import pygame_menu
from pygame_menu import sound

class Menu():
    def __init__(self, game):
        self.game = game
        self.DISPLAY_W, self.DISPLAY_H = self.game.DISPLAY_W, self.game.DISPLAY_H

        self.theme = self.own_theme()

        self.menu = pygame_menu.Menu('Common one', 
                                    self.DISPLAY_W, self.DISPLAY_H,
                                    theme=self.theme,
                                    onclose=pygame_menu.events.EXIT)
        self.aboutmenu = pygame_menu.Menu('About', 
                                    self.DISPLAY_W, self.DISPLAY_H, 
                                    theme=self.theme)

    
    def own_theme(self):
        """
        Настройка предустановленной темы pygame_menu
        """
        theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
        return theme


    
    def draw_buttons(self):
        """
        Задание элементов главного меню, а также доп.меню
        """
        engine = sound.Sound()
        engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'bg_sound/ms_click.ogg')
        engine.set_sound(sound.SOUND_TYPE_CLICK_TOUCH, 'bg_sound/ms_click.ogg')

        ABOUT = 'Some info about game'
        self.aboutmenu.add.label(ABOUT, max_char = -1, font_size = 20)
        self.aboutmenu.add.button('Return to main menu', pygame_menu.events.BACK)

        self.menu.set_sound(engine, recursive=True)
        self.menu.add.button('Connect', self.start_game)
        self.menu.add.text_input('IP: ', default='192.168.0.0', maxchar=15)
        self.menu.add.button('About', self.aboutmenu)
        self.menu.add.button('Exit', pygame_menu.events.EXIT)

        

    def on_resize(self):
        """
        (Не применяется) Динамическое изменение размеров элементов при изменение размеров окна
        """
        window_size = self.game.get_size()
        new_w, new_h = 0.75 * window_size[0], 0.7 * window_size[1]
        self.menu.resize(new_w, new_h)

    
    def open_menu(self):
        """
        Запуск главного меню
        """
        self.menu.mainloop(self.game.window)

    
    def start_game(self):
        """
        Запуск игры
        """
        self.game.playing = True
        self.game.game_loop()


        
    
