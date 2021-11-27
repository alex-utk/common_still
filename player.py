import pygame

class Player:
    UniqueID = 0 # Глобальный счетчик ID
    def __init__(self, name: str, path_to_avatar: str=None, connection: str=None):
        if not isinstance(name, str):
            raise TypeError(f"name must be {str}. {type(name)} was given")
        if not isinstance(path_to_avatar, (str, type(None))):
            raise TypeError(f"path_to_avatar must be {str} or {type(None)}. {type(path_to_avatar)} was given")
        if not isinstance(connection, (str, type(None))):
            raise TypeError(f"connection must be {str} or {type(None)}. {type(connection)} was given")
        
        self._name = name                                           # Имя игрока
        self._path_to_avatar = path_to_avatar                       # Путь к аватвру
        if path_to_avatar != None:
            self._avatar = pygame.image.load(self._path_to_avatar)  # Аватар
        self._connection = connection                               # Строка подключения
        self._points = []                                           # Очки насчитанные игроку на каждом раунде
        self._score = 0                                             # Общий счетчик очков
        self._answers = []                                          # Ответы данные игроком
        self._id = Player.UniqueID                                  # Персональный ID игрока
        Player.UniqueID += 1                                        # Инкрементирование глобального счетчика ID

    def isAnswerGiven(self, i: int) -> bool:
        '''
            Проверка дан ли игроком i-й ответ
        '''

        if not isinstance(i, int):
            raise TypeError(f"i must be {int}. {type(i)} was given")
        
        return (i < len(self._answers))

    def drawPlayer(self) -> pygame.image:
        '''
            Вывод аватара игрока        
        '''    

        if self._path_to_avatar is None:
            raise ValueError("path_to_avatar is required to be set")

        return self._avatar
    
    def addPoints(self, x: int):
        '''
            Установка 'x' очков игроку за последний раунд
        '''

        if not isinstance(x, int):
            raise TypeError(f"x must be {int}. {type(x)} was given")
        
        self._points.append(x)
        self._score += x

    def changePoints(self, x: int, i: int) -> None:
        '''
            Установка 'x' очков игроку за i-й раунд
        '''

        if not isinstance(i, int):
            raise TypeError(f"i must be {int}. {type(i)} was given")
        if not isinstance(x, int):
            raise TypeError(f"x must be {int}. {type(x)} was given")
        if i >= len(self._points):
            raise IndexError("Given index out of range")
        
        self._score -= self._points[i]
        self._points[i] = x
        self._score += x
    
    def addAnswer(self, answer: str) -> None:
        '''
            Установка последнего ответа игрока
        '''

        if not isinstance(answer, str):
            raise TypeError(f"answer must be {str}. {type(answer)} was given")

        self._answers.append(answer)

    def getAnswer(self, i: int) -> str:
        '''
            Вывод i-го овета игрока
        '''

        if not isinstance(i, int):
            raise TypeError(f"i must be {int}. {type(i)} was given")
        if i >= len(self._answers):
            raise IndexError("Given index out of range")
        
        return self._answers[i]

    @property
    def score(self) -> int:
        '''
            Вывод общего счета
        '''
        
        return self._score

    @property
    def points(self) -> list[int]:
        '''
            Вывод счета игрока по раундам
        '''

        return self._points
    @points.setter
    def points(self, points: list[int]) -> None:
        '''
            Установка массива очков игроку
        '''

        if not isinstance(points, list):
            raise TypeError(f"points must be {list[int]}. {type(points)} was given")

        self._points = []
        self._score = 0
        for point in points:
            if not isinstance(point, int):
                raise TypeError(f"element of points must be {int}. {type(point)} was given")

            self._points.append(point)
            self._score += point

    @property
    def answers(self) -> list[str]:
        '''
            Вывод ответов игрока
        '''

        return self._answers
    @answers.setter
    def answers(self, answers: list[str]) -> None:
        '''
            Установка ответов игрока
        '''

        if not isinstance(answers, list):
            raise TypeError(f"answers must be {list[str]}. {type(answers)} was given")
        
        self._answers = []
        for answer in answers:
            if not isinstance(answer, str):
                raise TypeError(f"element of points must be {str}. {type(answer)} was given")

            self._answers.append(answer)
    
    @property
    def name(self) -> str:
        '''
            Вывод имени игрока
        '''

        return self._name
    @name.setter
    def name(self, name: str):
        '''
            Установка имени игрока
        '''
        
        if not isinstance(name, str):
            raise TypeError(f"name must be {str}. {type(name)} was given")
        
        self._name = name

    @property
    def path_to_avatar(self) -> str:
        '''
            Вывод пути к файлу аватара игрока
        '''

        return self._path_to_avatar
    @path_to_avatar.setter
    def path_to_avatar(self, path_to_avatar: str) -> None:
        '''
            Установка пути к файлу аватара игрока и изменение аватара
        '''

        if not isinstance(path_to_avatar, str):
            raise TypeError(f"path_to_avatar must be {str}. {type(path_to_avatar)} was given")
        
        self._path_to_avatar = path_to_avatar
        self._avatar = pygame.image.load(path_to_avatar)

    @property
    def avatar(self) -> pygame.image:
        '''
            Вывод аватара игрока
        '''

        if self._path_to_avatar is None:
            raise ValueError("path_to_avatar is required to be set")

        return self._avatar

    @property
    def connection(self) -> str:
        '''    
            Вывод строки подключения
        '''

        return self._connection
    @connection.setter
    def connection(self, connection: str) -> None:
        '''
            Установка строки подключения
        '''

        if not isinstance(connection, str):
            raise TypeError(f"connection must be {str}. {type(connection)} was given")

        self._connection = connection
    
    @property
    def ID(self) -> int:
        '''
            Вывод ID игрока
        '''

        return self._id
