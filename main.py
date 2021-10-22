from game import Game
from menu import Menu

g = Game()
m = Menu(g)

while g.running:
    m.draw_buttons()
    m.open_menu()