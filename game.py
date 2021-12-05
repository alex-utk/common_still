import pygame
import gameClass
import os
import pygame_menu
import pygamevideo



class Game():
    def __init__(self, fps = 60, roundCnt = 2):
        pygame.init()
        self.gameStage = "prepare game"
        self.roundStage = "start"
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'img')
        self.running, self.playing = True, False    #Статусы Игра работает\Игра запущена
        self.DISPLAY_W, self.DISPLAY_H = 1600, 1000   #Размеры окна width и height
        self.fps = fps
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), flags = pygame.NOFRAME)
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        gameClass.font_name = pygame_menu.font.FONT_COMIC_NEUE
        self.startButton = gameClass.Button(x = 800, y = 500, Width = 200, Height = 100, text = "Start Gasme", on_click = self.StartGame)
        self.skipButton = gameClass.Button(x = 60, y = 25, Width = 120, Height = 50, text = "Skip video", on_click = self.Skip)
        self.timer = gameClass.timerSprite(x = 800, y = 500, Width = 800, Height = 200, fps = self.fps, text = "It's time to give answer!!!")
        self.markSurf = gameClass.CleverSurf()
        self.snipSurf1 = gameClass.CleverSurf()
        self.snipSurf2 = gameClass.CleverSurf()
        self.snipSurf3 = gameClass.CleverSurf()
        surf = pygame.Surface((1200, 600))
        surf.fill((255,255,255))
        self.plug =  gameClass.CleverSurf(surf, surf.get_rect(), 800, 500)
        self.markButton = gameClass.Button(975, 600, 120, 50, "ok", self.SetMark)
        self.inputBox = gameClass.InputBox(770, 575, 120, 50)
        self.nickSurf = gameClass.CleverSurf()
        self.ansSurf = gameClass.CleverSurf()
        text_surf, text_rect = gameClass.draw_text("says the answer is", 30, 900, 450, "center")
        self.textSurf = gameClass.CleverSurf(text_surf, text_rect)
        self.sprites = [gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "1", 120, 180, 100, 500),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "2", 120, 180, 1500, 500),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "3", 120, 180, 800, 100),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "4", 120, 180, 600, 900),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "5", 120, 180, 1000, 900),
                       self.startButton, self.skipButton, self.timer, self.plug, self.markSurf, self.snipSurf1, self.snipSurf2, self.snipSurf3, self.textSurf,
                       self.ansSurf, self.nickSurf, self.inputBox, self.markButton]
        self.currPlayer = 0
        self.roundCnt = roundCnt
        self.currRound = 0
        self.video = None
   
    def SetPlayer(self):
        #получаю игроков из телеги
        playerName = ["1", "2", "3", "4", "5"]
        self.playerCnt = len(playerName)
        #  гружу в список
        for i in range(len(playerName)):
            self.sprites[i].name = playerName[i]
            self.sprites[i].viseble = True

    def StartGame(self, button):
        self.gameStage = "game in process"
        self.roundStage = "start"
        self.startButton.viseble = False
        # отправит сообщение в бота

    def AnswerGiven(self, timer):
        self.roundStage = "stop answer"
        self.timer.viseble = False
        # отправит сообщение в бота
    
    def Skip(self, button):
        self.video.seek_time(self.video.duration)
    
    def SetMark(self, button):
        player = self.sprites[self.currPlayer]
        player.score += int(self.inputBox.text)
        self.inputBox.text = ""
        self.currPlayer += 1
    
    def DoMark(self):
        if self.currPlayer < len(self.answer):
            answer = self.answer[self.currPlayer]
            nickname = self.sprites[self.currPlayer].name
            self.markSurf.surf = self.sprites[self.currPlayer].playerImage
            self.markSurf.rect = self.sprites[self.currPlayer].playerImageRect
            self.markSurf.size = (200, 300)
            self.markSurf.pos = (650, 500)
            self.markSurf.viseble = True
            self.textSurf.viseble = True
            nick_surf, nick_rect = gameClass.draw_text(nickname, 30, 900, 375, "center")
            self.nickSurf.surf = nick_surf
            self.nickSurf.rect = nick_rect
            self.nickSurf.viseble = True
            answer_surf, answer_rect = gameClass.draw_text(answer, 30, 900, 525, "center")
            self.ansSurf.surf = answer_surf
            self.ansSurf.rect = answer_rect
            self.ansSurf.viseble = True
        else:
            self.roundStage = "start"

    def DoGameProcc(self):
        if self.roundStage == "start":
            if self.currRound < self.roundCnt:
                self.videopath, self.timecode = next(self.roundIter)
                self.video = pygamevideo.Video(self.videopath, (200, 200))
                self.video.set_size((1200, 600))
                self.video.play()
                frame = self.video.getFrameForTime(self.timecode[0])
                self.snipSurf1.surf = frame
                self.snipSurf1.size = (500, 250)
                self.snipSurf1.pos = (300, 825)
                frame = self.video.getFrameForTime(self.timecode[1])
                self.snipSurf2.surf = frame
                self.snipSurf2.size = (500, 250)
                self.snipSurf2.pos = (1300, 825)
                frame = self.video.getFrameForTime(self.timecode[2])
                self.snipSurf3.surf = frame
                self.snipSurf3.size = (500, 250)
                self.snipSurf3.pos = (800, 175)
                self.skipButton.viseble = True
                for i in range(self.playerCnt):
                    self.sprites[i].viseble = True
                self.plug.viseble = False
                self.snipSurf1.viseble = False
                self.snipSurf2.viseble = False
                self.snipSurf3.viseble = False
                self.inputBox.viseble = False
                self.markButton.viseble = False
                self.nickSurf.viseble = False
                self.ansSurf.viseble = False
                self.markSurf.viseble = False
                self.textSurf.viseble = False
                self.currRound += 1
                self.roundStage = "playingRound"
            else:
                self.gameStage = "end game"
        elif self.roundStage == "playingRound" and not self.video.is_playing:
           self.roundStage = "give answer"
           self.video.stop()
           self.skipButton.viseble = False
        elif self.roundStage == "give answer":
            self.timer.viseble = True
            if not self.timer.on:
                self.timer.timerStart(2, self.AnswerGiven)
        elif self.roundStage == "stop answer":
            self.currPlayer = 0
            self.answer = ["1", '2', '3', '4', '5']
            for i in range(self.playerCnt):
                self.sprites[i].viseble = False
            self.plug.viseble = True
            self.snipSurf1.viseble = True
            self.snipSurf2.viseble = True
            self.snipSurf3.viseble = True
            self.inputBox.viseble = True
            self.markButton.viseble = True
            self.roundStage = "mark answer"
        elif self.roundStage == "mark answer":
            self.DoMark()

    def game_loop(self):
        """
        Запуск основного игрового цикла
        """
        # подготовка игры
        self.roundIter = gameClass.RoundIter(self.roundCnt)
        gameCode = gameClass.draw_text("AAAA", 50, 1500, 0)
        self.currRound = 0
        self.gameStage = "prepare game"
        self.roundStage = "start"
        self.button = [self.startButton, self.skipButton, self.markButton]
        self.video = None
        clock = pygame.time.Clock()
        for sprite in self.sprites:
            sprite.viseble = False
        self.startButton.viseble = True
        while self.playing:
            clock.tick(self.fps)

            self.check_events()
            
            if self.gameStage == "prepare game":
                #подготовка к игре
                self.SetPlayer()
            elif self.gameStage == "game in process":
                #показ игры
                self.DoGameProcc()
            elif self.gameStage == "end game":
                self.sprites.clear()
                self.video = None

            for sprite in self.sprites:
                sprite.update()


            self.display.fill(self.WHITE)
            self.display.blit(gameCode[0], gameCode[1])
            self.window.blit(self.display, (0, 0))
            if self.video != None:
                self.video.draw(self.window)
            for sprite in self.sprites:
                sprite.draw(self.window)
            pygame.display.flip()
            self.reset_keys()  

    def check_events(self):
        """
        Проверка событий совершенных игроком
        """
        self.reset_keys()
        for event in pygame.event.get():
            for button in self.button:
                button.handle_mouse_event(event.type, pygame.mouse.get_pos())
            self.inputBox.handle_event(event)
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.EXIT_KEY, self.playing = True, False
                    if self.video != None:
                        self.video.stop()
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

    def get_size(self):
        """
        Получить размеры игрового окна
        """
        return self.DISPLAY_W, self.DISPLAY_H