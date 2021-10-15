class Player:
    def __init__(self, name, avatar=None):
        self.name = name
        self.avatar = avatar
        self._points = []
        self._score = 0
        self.answers = []
    
    def addPoints(self, x):
        self._points.append(x)
        self._score += x

    def changePoints(self, x, i):
        self._score -= self._points[i]
        self._points[i] = x
        self._score += x

    def getScore(self):
        return self._score