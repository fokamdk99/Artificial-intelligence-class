import pygame as pg
import sys
import time
from pygame.locals import *
from stan import State
from minimax import minimax
import copy

width = 400
height = 400
white = (255,255,255)
blue = (0,0,255)
line_color = (0,0,0)

#initiate game window
pg.init()
pg.font.init()
font = pg.font.SysFont("Comic Sans MS", 20)
#set frame rate
fps = 30

#measure time
timer = pg.time.Clock()

#set size of window
screen = pg.display.set_mode((width, height+100), 0, 32)

#set caption
pg.display.set_caption("TIC TAC TOE game")

x_image = pg.image.load("x.png")
o_image = pg.image.load("o.png")

x_image = pg.transform.scale(x_image, (90,90))
o_image = pg.transform.scale(o_image, (90,90))

def home_window(actual_state):
    screen.fill(white)
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 
   
    # drawing horizontal lines 
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 
    draw_status(actual_state, True)
    pg.display.update()

def draw_status(actual_state, turn):
    message = "brak"
    if turn:
        message = "Your turn"
    else:
        message = "Opponent's turn"
    if actual_state.terminal and actual_state.winner == "p":
        message = "You won!"
    elif actual_state.terminal and actual_state.winner == "o":
        message = "Opponent won!"
    elif actual_state.terminal and actual_state.winner == "-":
        message = "It's a tie!"
    
    text = font.render(message, 1, blue)
    screen.fill ((0, 0, 0), (0, 400, 500, 100)) 
    text_rect = text.get_rect(center =(width / 2, 500-50)) 
    screen.blit(text, text_rect) 
    pg.display.update() 

def draw_state(actual_state):
    for row in range(0,3):
        for column in range(0,3):
            player_type = actual_state.board[row][column]
            x = column*width/3 + 30
            y = row*height/3 + 30
            if player_type == "p":
                screen.blit(x_image, (x, y))
            elif player_type == "o":
                screen.blit(o_image, (x, y))
    pg.display.update()

def user_click(actual_state):
    x, y = pg.mouse.get_pos()

    x = int(x/(width/3))
    y = int(y/(height/3))

    if actual_state.board[y][x] == "-":
        return y,x,True
    
    return y,x,False

def main():
    actual_state = State(True)
    home_window(actual_state)

    while(True):
        
        #draw_state(actual_state)
        make_move = False

        for event in pg.event.get(): 
            if event.type == QUIT: 
                return
            if event.type == MOUSEBUTTONDOWN:
                x,y,make_move = user_click(actual_state)
                if make_move:
                    actual_state = actual_state.make_move(x,y)
                    draw_state(actual_state)
                    draw_status(actual_state, False)
                    time.sleep(2)
                    if actual_state.terminal:
                        break
                    else:
                        U = actual_state.get_successors()
                        index = minimax(actual_state, 4, False, 4)
                        actual_state = State(not U[index].max_player, copy.deepcopy(U[index].board))
                        draw_state(actual_state)
                        draw_status(actual_state, True)
                    if actual_state.terminal:
                        break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    return

        if actual_state.terminal:
            actual_state = State(True)
            home_window(actual_state)
                
        
        pg.display.update() 

main()