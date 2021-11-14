class Room:
    def __init__(self):
        self.UID = -1 #Уникальный идентификатор комнаты, формат AAAA, 4 латинские буквы
        self.Users = [] #Массив id пользователей данной комнаты
    
    def insert(self, x):
        """
        Вставка нового пользователя
        """
        self.Users.append(x)

    def remove(self, x):
        """
        Удаление пользователя 
        """
        self.Users.remove(x)

    def count(self):
        """
        Вернуть текущее количество пользователей
        """
        return len(self.Users)

    def clear(self):
        """
        Очистить список пользователей
        """
        self.Users.clear()

    def setUID(self, x):
        self.UID = x