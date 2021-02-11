'''
aby wprowadzic ruch, nalezy kolejno podac numer wiersza oraz numer kolumny.
Obydwie wartosci musza zawierac sie w zbiorze [0, 1, 2]
'''

from stan import State
from minimax import minimax
import copy
import random

def __main__():
    max_player = True
    s = State(max_player)
    while(True):
        print("\n\ntwoj ruch!")
        
        s = s.make_move()
        s.show_board()
        if game_over(s):
            break
        print("\n\nruch przeciwnika!")
        U = s.get_successors()
        index = minimax(s, 4, not max_player, 4)
        s = State(not U[index].max_player, copy.deepcopy(U[index].board))
        s.show_board()
        if game_over(s):
            break

def game_over(s):
    if s.terminal and s.winner == "p":
        print("Gra zakonczona! Wygrana gracza")
        return True
    elif s.terminal and s.winner == "o":
        print("Gra zakonczona! Wygrana przeciwnika")
        return True
    elif s.terminal and s.winner == "-":
        print("Gra zakonczona! Remis")
        return True
    return False

__main__()