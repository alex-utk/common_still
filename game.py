import pygame
import gameClass
import os
import pygame_menu
import pygamevideo
import WebHook

class Game():
    def __init__(self, fps = 60, roundCnt = 2):
        pygame.init()
        self.gameStage = "prepare game"
        self.roundStage = "start"
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'img')
        self.bg = pygame.image.load(os.path.join(self.img_folder, 'bg.jpg'))
        self.running, self.playing = True, False    #Статусы Игра работает\Игра запущена
        self.DISPLAY_W, self.DISPLAY_H = 1600, 1000   #Размеры окна width и height
        self.fps = fps
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), flags = pygame.NOFRAME)
        self.bg = pygame.transform.scale(self.bg.convert(), (1600, 1000))
        self.frame = pygame.image.load(os.path.join(self.img_folder, 'frame.png'))
        self.frame = gameClass.CleverSurf(self.frame, self.frame.get_rect())
        self.frame.pos = (800, 500)
        self.bgRect = self.bg.get_rect()
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        #data initialization
        gameClass.font_name = pygame_menu.font.FONT_COMIC_NEUE
        self.startButton = gameClass.Button(x = 800, y = 500, Width = 200, Height = 100, text = "Start Game", on_click = self.StartGame)
        self.skipButton = gameClass.Button(x = 60, y = 25, Width = 120, Height = 50, text = "Skip video", on_click = self.Skip)
        self.timer = gameClass.timerSprite(x = 800, y = 500, Width = 800, Height = 200, fps = self.fps, text = "It's time to give answer!!!")
        self.markSurf = gameClass.CleverSurf()
        self.snipSurf1 = gameClass.CleverSurf()
        self.snipSurf2 = gameClass.CleverSurf()
        self.snipSurf3 = gameClass.CleverSurf()
        surf = pygame.Surface((1200, 600))
        surf.fill((255,255,255))
        self.markButton = gameClass.Button(975, 600, 120, 50, "ok", self.SetMark)
        self.inputBox = gameClass.InputBox(770, 575, 120, 50)
        self.nickSurf = gameClass.CleverSurf()
        self.ansSurf = gameClass.CleverSurf()
        text_surf, text_rect = gameClass.draw_text("says the answer is", 30, 900, 450, "center")
        self.textSurf = gameClass.CleverSurf(text_surf, text_rect)
        leder_surf, leder_rect = gameClass.draw_text("Winner !!! Well, now let's disperse, get out of here", 30, 800, 650, "center")
        self.mesSurf = gameClass.CleverSurf(leder_surf, leder_rect)
        self.sprites = [gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "No one", 120, 180, 800, 75),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "1", 120, 180, 1500, 500),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "2", 120, 180, 1000, 875),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "3", 120, 180, 600, 875),
                       gameClass.PlayerSprites(pygame.image.load(os.path.join(self.img_folder, '11.png')).convert(), "4", 120, 180, 100, 500),
                       self.startButton, self.skipButton, self.timer, self.frame, self.markSurf, self.snipSurf1, self.snipSurf2, self.snipSurf3, self.textSurf,
                       self.ansSurf, self.nickSurf, self.inputBox, self.markButton, self.mesSurf]
        self.currPlayer = 0
        self.roundCnt = roundCnt
        self.currRound = 0
        self.video = None
        WebHook.webGame.createRoom()
   
    def SetPlayer(self):
        #Loading players
        playerName = WebHook.webGame.return_users()
        self.playerCnt = len(playerName)
        for i in range(5):
            self.sprites[i].visible = False
        for i in range(len(playerName)):
            self.sprites[i].name = playerName[i]
            self.sprites[i].visible = True

    def StartGame(self, button):
        self.gameStage = "game in process"
        self.roundStage = "start"
        self.startButton.visible = False
        WebHook.webGame.start_game()

    def AnswerGiven(self, timer):
        self.roundStage = "stop answer"
        self.timer.visible = False
        self.frame.visible = False
        WebHook.webGame.stop_round()
    
    def Skip(self, button):
        self.video.seek_time(self.video.duration)
    
    def SetMark(self, button):
        nickname = self.answer[self.currPlayer][0]
        ind = 0
        for i in range(5):
            if self.sprites[i].name == nickname:
                ind = i
        player = self.sprites[ind]
        try:
            player.score += int(self.inputBox.text)
        except ValueError:
            return
        self.inputBox.text = ""
        self.currPlayer += 1
    
    def DoMark(self):
        if self.currPlayer < len(self.answer):
            answer = self.answer[self.currPlayer][1]
            nickname = self.answer[self.currPlayer][0]
            ind = 0
            for i in range(5):
                if self.sprites[i].name == nickname:
                    ind = i
            self.markSurf.surf = self.sprites[ind].playerImage
            self.markSurf.rect = self.sprites[ind].playerImageRect
            self.markSurf.size = (200, 300)
            self.markSurf.pos = (650, 500)
            self.markSurf.visible = True
            self.textSurf.visible = True
            nick_surf, nick_rect = gameClass.draw_text(nickname, 30, 900, 375, "center")
            self.nickSurf.surf = nick_surf
            self.nickSurf.rect = nick_rect
            self.nickSurf.visible = True
            answer_surf, answer_rect = gameClass.draw_text(answer, 30, 900, 525, "center")
            self.ansSurf.surf = answer_surf
            self.ansSurf.rect = answer_rect
            self.ansSurf.visible = True
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
                self.skipButton.visible = True
                for i in range(self.playerCnt):
                    self.sprites[i].visible = True
                self.frame.visible = True
                self.snipSurf1.visible = False
                self.snipSurf2.visible = False
                self.snipSurf3.visible = False
                self.inputBox.visible = False
                self.markButton.visible = False
                self.nickSurf.visible = False
                self.ansSurf.visible = False
                self.markSurf.visible = False
                self.textSurf.visible = False
                self.currRound += 1
                self.roundStage = "playingRound"
            else:
                self.gameStage = "end game"
        elif self.roundStage == "playingRound" and not self.video.is_playing:
           self.roundStage = "give answer"
           self.video.stop()
           self.skipButton.visible = False
        elif self.roundStage == "give answer":
            self.timer.visible = True
            if not self.timer.on:
                WebHook.webGame.start_round()
                self.timer.timerStart(30, self.AnswerGiven)
        elif self.roundStage == "stop answer":
            self.currPlayer = 0
            self.answer = WebHook.webGame.return_answers()
            for i in range(self.playerCnt):
                self.sprites[i].visible = False
            self.snipSurf1.visible = True
            self.snipSurf2.visible = True
            self.snipSurf3.visible = True
            self.inputBox.visible = True
            self.markButton.visible = True
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
            sprite.visible = False
        self.startButton.visible = True
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
                ind = 0
                for i in range(5):
                    if self.sprites[i].score > self.sprites[ind].score:
                        ind = i
                for sprite in self.sprites:
                    sprite.visible = False
                self.markSurf.surf = self.sprites[ind].playerImage
                self.markSurf.size = (350, 400)
                self.markSurf.pos = (800, 400)
                nick_surf, nick_rect = gameClass.draw_text(self.sprites[ind].name, 30, 800, 625, "center")
                self.nickSurf.surf = nick_surf
                self.nickSurf.rect = nick_rect
                self.nickSurf.visible = True
                self.mesSurf.visible = True
                self.markSurf.visible = True
                self.video = None

            for sprite in self.sprites:
                sprite.update()
            
            self.display.fill(self.WHITE)
            self.display.blit(self.bg, self.bgRect)
            self.display.blit(gameCode[0], gameCode[1])
            self.window.blit(self.display, (0, 0))
            if self.video != None and self.roundStage != "mark answer":
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
                    self.timer.visible = False
                    self.timer.on = False
                    self.gameStage = "prepare game"
                    WebHook.webGame.stop_game()
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