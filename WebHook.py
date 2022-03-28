from logging import raiseExceptions
from Ans import Answer
from datetime import datetime
from WebGamePart import WebGamePart
import telebot
from room import Room
#from telebot import type

# Bot TOKEN
TOKEN = '1757432372:AAHNMbgLfYR6Yb4nR76cAY67Voju8MGTzpQ'

#Набор игровой информации и команд для общения с игровым циклом 
webGame = WebGamePart()

#Доступные команды
commands = {
    'create_room'       : 'Create new room',
    'join_room'         : 'Join existing room',
    'exit_room'         : 'Exit current room',
    'send_ans'          : 'Send answer to current question',
    'help'              : 'Show available commands'
}

bot = telebot.TeleBot(TOKEN) #Создание бота
#m,aermhaemherh

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Обернуть все в класс WebGamePart
#Получение списка id игроков + Ник неймы
#Список ответов игроков "игрок,ответ" str[]
#Переменная, что игра началась или нет
#Переменная, что можно скидывать ответ
#Команда: получение ответов, можно отвечать, нельзя отвечать, игра началась, игра закончилась, 
#   получение списка ответов, получение списка пользователей
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def check_user(id):
    """
    Проверка состоит ли пользователь в какой-либо комнате,
    Если да - вернуть её номер
    Если нет - вернуть -1
    """
    f = -1
    n = len(webGame.knownRooms)
    for i in range(n):
        m = webGame.knownRooms[i].count()
        for j in range(m):
            if webGame.knownRooms[i].UsersID[j] == id:
                f = webGame.knownRooms[i].UID
                break
    return f


@bot.message_handler(commands=['create_room'])
def command_create_room(m):
    """
    Обработка команды создания комнаты, её очищение, присваивание UID
    """
    id = m.from_user.id
    buf = Room()
    #Заглушка, создание UID для комнаты на основе порядка её создания в боте
    buf.setUID(len(webGame.knownRooms) + 1)
    buf.set_lead(id)
    bot.send_message(id, 'Room created, Room UID: {}'.format(buf.UID))
    webGame.knownRooms.append(buf)


@bot.message_handler(commands=['join_room'])
def command_join_room(m):
    """
    Обработка команды присоединения пользователя к комнате
    """
    id = m.from_user.id
    #Проверить не находится ли пользователь уже в какой-либо комнате
    check1 = check_user(id)
    if check1 != -1:
        bot.send_message(id, 'You are already in the room {}'.format(check1))
        return

    mes_text = m.text[10:]
    text = mes_text.split()
    numBuf = int(text[0])
    nick = text[1]
    #Добавить обработку ошибки при неправильном номере комнаты!!!!
    n = len(webGame.knownRooms)
    check2 = True
    for i in range(n):
        if webGame.knownRooms[i].UID == numBuf:
            webGame.knownRooms[i].insert(id, nick)
            check2 = False
    if check2:
        bot.send_message(id, 'Room with UID {}, does not exist'.format(numBuf))
        return
    bot.send_message(id, 'You successfully joined Room: {}, your ID: {}'.format(numBuf, id))


@bot.message_handler(commands=['exit_room'])
def command_exit_room(m):
    """
    Обработка команды выхода из комнаты
    """
    id = m.from_user.id
    nick = None
    b = True
    for i in range(len(webGame.knownRooms)):
        for j in range(len(webGame.knownRooms[i].UsersID)):
            if id == webGame.knownRooms[i].UsersID[j]:
                nick = webGame.knownRooms[i].UsersNick[j]
    #Проверить не находится ли пользователь уже в какой-либо комнате
    check1 = check_user(id)
    if check1 == -1:
        bot.send_message(id, 'You havent entered the Room yet')
        return

    mes_text = m.text[10:]
    #numBuf = int(mes_text)
    #Добавить обработку ошибки при неправильном номере комнаты!!!!
    webGame.knownRooms[check1 - 1].remove(id, nick)
    bot.send_message(id, 'You successfully exited Room: {}, your nick: {}'.format(check1 - 1, nick))  


@bot.message_handler(commands=['send_ans'])
def command_send_ans(m):
    """
    Обработка команды принятия ответа пользователя
    """
    id = m.from_user.id

    if webGame.IsPlaying == False:
        bot.send_message(id, 'Game has not started')
        return
    else:
        if webGame.IsGivingAnswers == False:
            bot.send_message(id, 'Game has started, but it is not time for answers')
            return

    nick = None
    b = True
    for i in range(len(webGame.knownRooms)):
        for j in range(len(webGame.knownRooms[i].UsersID)):
            if id == webGame.knownRooms[i].UsersID[j]:
                nick = webGame.knownRooms[i].UsersNick[j]
    mes_text = m.text[9:]
    webGame.add_answer(Answer(mes_text, id, nick, datetime.now()))

    check1 = check_user(id)
    if check1 == -1:
        bot.send_message(id, 'You havent entered the Room yet')
        return
    bot.send_message(id, 'user:{} - Your answer successfully send'.format(nick))


@bot.message_handler(commands=['help'])
def command_help(m):
    """
    Обработка команды помощи пользователю
    """
    id = m.from_user.id
    help_text = "The following commands are available: \n"
    for key in commands:  
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(id, help_text)  

@bot.message_handler(commands=['test'])
def command_test(m):
    """
    Тестирование работы класса WebGamePart
    """
    id = m.from_user.id
    text = "Users: \n"
    for key in webGame.return_users():  
        text += key + '\n'
    bot.send_message(id, text)  

    text = "Answers: \n"
    for key in webGame.return_answers():  
        text += key + '\n'
    bot.send_message(id, text)  

@bot.message_handler(commands=['sg'])
def command_sg(m):
    webGame.start_game()

@bot.message_handler(commands=['sr'])
def command_sr(m):
    webGame.start_round() 
