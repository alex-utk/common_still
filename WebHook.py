from room import Room
import telebot
#from telebot import type

# Bot TOKEN
TOKEN = '1757432372:AAHNMbgLfYR6Yb4nR76cAY67Voju8MGTzpQ'

#Список комнат
knownRooms = []

#Доступные команды
commands = {
    'create_room'       : 'Create new room',
    'join_room'         : 'Join existing room',
    'exit_room'         : 'Exit current room',
	'rooms'	            : 'Show amount of the rooms and amount of users in each one',
    'send_ans'          : 'Send answer to current question',
    'help'              : 'Show available commands'
}

bot = telebot.TeleBot(TOKEN) #Создание бота

def check_user(id):
    """
    Проверка состоит ли пользователь в какой-либо комнате,
    Если да - вернуть её номер
    Если нет - вернуть -1
    """
    f = -1
    n = len(knownRooms)
    for i in range(n):
        m = knownRooms[i].count()
        for j in range(m):
            if knownRooms[i].Users[j] == id:
                f = knownRooms[i].UID
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
    buf.setUID(len(knownRooms) + 1)
    buf.set_lead(id)
    bot.send_message(id, 'Room created, Room UID: {}'.format(buf.UID))
    knownRooms.append(buf)


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
    numBuf = int(mes_text)
    #Добавить обработку ошибки при неправильном номере комнаты!!!!
    n = len(knownRooms)
    check2 = True
    for i in range(n):
        if knownRooms[i].UID == numBuf:
            knownRooms[i].insert(id)
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
    #Проверить не находится ли пользователь уже в какой-либо комнате
    check1 = check_user(id)
    if check1 == -1:
        bot.send_message(id, 'You havent entered the Room yet')
        return

    mes_text = m.text[10:]
    numBuf = int(mes_text)
    #Добавить обработку ошибки при неправильном номере комнаты!!!!
    knownRooms[check1].remove(id)
    bot.send_message(id, 'You successfully exited Room: {}, your ID: {}'.format(numBuf, id))  

@bot.message_handler(commands=['rooms'])
def command_rooms(m):
    """
    Обработка команды демонстрации информации о комнатах
    """
    id = m.from_user.id
    n = len(knownRooms)
    mes_text = 'There are total: {} Rooms now\n'.format(n)
    for i in range(n):
        buf = 'Room: {}, Users: {}\n'.format(knownRooms[i].UID, knownRooms[i].count())
        mes_text += buf
    bot.send_message(id, mes_text)

@bot.message_handler(commands=['send_ans'])
def command_send_ans(m):
    """
    Обработка команды принятия ответа пользователя
    """
    id = m.from_user.id
    mes_text = m.text[9:]
    check1 = check_user(id)
    if check1 == -1:
        bot.send_message(id, 'You havent entered the Room yet')
        return
    room_id = 0
    for i in range(len(knownRooms)):
        if knownRooms[i].UID == check1:
            room_id = knownRooms[i].lead
    bot.send_message(room_id, 'user:{} ans:{}'.format(id, mes_text))
    bot.send_message(id, 'user:{} - Your answer succsessuly send'.format(id))

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


#Start message handling
bot.polling()