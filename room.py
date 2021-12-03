class Room:
    def __init__(self):
        self.UID = -1 #Уникальный идентификатор комнаты, формат AAAA, 4 латинские буквы
        self.UsersID = [] #Массив id пользователей данной комнаты
        self.UsersNick = [] #Массив nick name пользователей данной комнаты
        self.lead = 0 #ID создателя комнаты

    def set_lead(self, x):
        """
        Установить лидера комнаты
        """
        self.lead = x
    
    def insert(self, x, y):
        """
        Вставка нового пользователя
        """
        self.UsersID.append(x)
        self.UsersNick.append(y)

    def remove(self, x, y):
        """
        Удаление пользователя 
        """
        self.UsersID.remove(x)
        self.UsersNick.remove(y)

    def count(self):
        """
        Вернуть текущее количество пользователей
        """
        return len(self.UsersID)

    def clear(self):
        """
        Очистить список пользователей
        """
        self.UsersID.clear()
        self.UsersNick.clear()

    def setUID(self, x):
        self.UID = x