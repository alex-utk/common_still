from logging import raiseExceptions
import telebot
from room import Room
from Ans import Answer

id_to_message = {
    0: 'Players we starting the game',
    1: 'It is time to give answers',
    2: 'Time to give answers ended',
    3: 'Player game has ended'
}


class WebGamePart:
    def __init__(self):
        self.knownRooms = [] #Комнаты
        self.IsGivingAnswers = False #Флаг можно ли давать ответы игрокам
        self.IsPlaying = False #Флаг началась ли игра
        self.Answers = [] #Массив ответов игроков
    
    def start_game(self):
        """
        Смена состояние на начало игры
        """
        self.IsPlaying = True

    def stop_game(self):
        """
        Смена состояние на прекращение игры
        """
        self.IsPlaying = False

    def start_round(self):
        """
        Смена состояние на начало раунда
        """
        self.IsGivingAnswers = True

    def stop_round(self):
        """
        Смена состояние на прекращение раунда
        """
        self.IsGivingAnswers = False

    def add_answer(self, ans):
        """
        Добавление ответа пользователя
        """
        self.Answers.append(ans)

    def clear_answer(self):
        """
        Очищение списков ответов
        """
        self.Answers.clear()

    def clear_users(self):
        """
        Очищение пользователей комнаты
        """
        self.knownRooms.clear()

    def send_message_to_room(self, UID, mes, bot):
        """
        Функция отправки сообщения mes всем пользователям комнаты с номером UID
        """
        f = False
        for i in range(len(self.knownRooms)):
            if self.knownRooms[i].UID == UID:
                f = True
                for j in range(len(self.knownRooms[i].UsersID)):
                    bot.send_message(self.knownRooms[i].UsersID[j], mes)
            else:
                continue
        if f == False:
            raiseExceptions('There is no room with UID: {}'.format(UID))

    def send_template_to_room(self, UID, mes_id, bot):
        """
        Функция отправки шаблонных сообщений mes всем пользователям комнаты с номером UID
        """
        f = False
        for i in range(len(self.knownRooms)):
            if self.knownRooms[i].UID == UID:
                f = True
                for j in range(len(self.knownRooms[i].UsersID)):

                    bot.send_message(self.knownRooms[i].UsersID[j], id_to_message[mes_id])
            else:
                continue
        if f == False:
            raiseExceptions('There is no room with UID: {}'.format(UID))

    def return_answers(self):
        """
        Получить список данных пользователями ответов,
        формат: <user_id> <user_nick> <user_answer_text>
        """
        buf = []
        for p in self.Answers:
            b = str(p.user) + ' ' + str(p.nick) + ' ' + str(p.text)
            buf.append(b)
        return buf

    def return_users(self):
        """
        Получить список пользователей
        формат: <user_id> <user_nick>
        """
        buf = []
        for i in range(self.knownRooms[0].count()):
            b = str(self.knownRooms[0].UsersID[i]) + ' ' + str(self.knownRooms[0].UsersNick[i])
            buf.append(b)
        return buf
