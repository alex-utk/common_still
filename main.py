from game import Game
from menu import Menu
import WebHook
import threading

t1 = threading.Thread(target=WebHook.bot.polling)
t1.start()
g = Game()
m = Menu(g)

while g.running:
    m.draw_buttons()
    m.open_menu()
