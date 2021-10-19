class Player:
    UniqueID = 0 # Глобальный счетчик ID
    def __init__(self, name: str, avatar: str=None, connection: str=None):
        if not isinstance(name, str):
            raise TypeError(f"name must be {str}. {type(name)} was given")
        if not isinstance(avatar, (str, type(None))):
            raise TypeError(f"avatar must be {str} or {type(None)}. {type(avatar)} was given")
        if not isinstance(connection, (str, type(None))):
            raise TypeError(f"connection must be {str} or {type(None)}. {type(connection)} was given")
        
        self._name = name               # Имя игрока
        self._avatar = avatar           # Аватар
        self._connection = connection   # Строка подключения
        self._points = []               # Очки насчитанные игроку на каждом раунде
        self._score = 0                 # Общий счетчик очков
        self._answers = []              # Ответы данные игроком
        self._id = Player.UniqueID      # Персональный ID игрока
        Player.UniqueID += 1            # Инкрементирование глобального счетчика ID

    # Проверка дан ли игроком i-й ответ
    def isAnswerGiven(self, i: int) -> bool:
        if not isinstance(i, int):
            raise TypeError(f"i must be {int}. {type(i)} was given")
        
        return (i < len(self._answers))

    # Прорисовка игрока в точке (x, y) экрана
    def drawPlayer(self, x: int, y: int) -> None:
        if not isinstance(x, int):
            raise TypeError(f"x must be {int}. {type(x)} was given")
        if not isinstance(y, int):
            raise TypeError(f"y must be {int}. {type(y)} was given")
        
        pass
    
    # Установить 'x' очков игроку за последний раунд
    def addPoints(self, x: int):
        if not isinstance(x, int):
            raise TypeError(f"x must be {int}. {type(x)} was given")
        
        self._points.append(x)
        self._score += x

    # Установить 'x' очков игроку за i-й раунд
    def changePoints(self, x: int, i: int) -> None:
        if not isinstance(i, int):
            raise TypeError(f"i must be {int}. {type(i)} was given")
        if not isinstance(x, int):
            raise TypeError(f"x must be {int}. {type(x)} was given")
        if i >= len(self._points):
            raise IndexError("Given index out of range")
        
        self._score -= self._points[i]
        self._points[i] = x
        self._score += x
    
    # Установить последний ответ игрока
    def addAnswer(self, answer: str) -> None:
        if not isinstance(answer, str):
            raise TypeError(f"answer must be {str}. {type(answer)} was given")

        self._answers.append(answer)

    # Получить i-й овет игрока
    def getAnswer(self, i: int) -> str:
        if not isinstance(i, int):
            raise TypeError(f"i must be {int}. {type(i)} was given")
        if i >= len(self._answers):
            raise IndexError("Given index out of range")
        
        return self._answers[i]

    # Общий счет
    @property
    def score(self) -> int:
        return self._score

    # Счет игрока по раундам
    @property
    def points(self) -> list[int]:
        return self._points
    @points.setter
    def points(self, points: list[int]) -> None:
        if not isinstance(points, list):
            raise TypeError(f"points must be {list[int]}. {type(points)} was given")

        self._points = []
        self._score = 0
        for point in points:
            if not isinstance(point, int):
                raise TypeError(f"element of points must be {int}. {type(point)} was given")

            self._points.append(point)
            self._score += point

    # Ответы игрока
    @property
    def answers(self) -> list[str]:
        return self._answers
    @answers.setter
    def answers(self, answers: list[str]) -> None:
        if not isinstance(answers, list):
            raise TypeError(f"answers must be {list[str]}. {type(answers)} was given")
        
        self._answers = []
        for answer in answers:
            if not isinstance(answer, str):
                raise TypeError(f"element of points must be {str}. {type(answer)} was given")

            self._answers.append(answer)
    
    # Имя игрока
    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f"name must be {str}. {type(name)} was given")
        
        self._name = name

    # Аватар игрока
    @property
    def avatar(self) -> str:
        return self._avatar
    @avatar.setter
    def avatar(self, avatar: str) -> None:
        if not isinstance(avatar, str):
            raise TypeError(f"avatar must be {str}. {type(avatar)} was given")
        
        self._avatar = avatar

    # Строка подключения игрока
    @property
    def connection(self) -> str:
        return self._connection
    @connection.setter
    def connection(self, connection: str) -> None:
        if not isinstance(connection, str):
            raise TypeError(f"connection must be {str}. {type(connection)} was given")

        self._connection = connection
    
    # ID игрока
    @property
    def ID(self) -> int:
        return self._id
