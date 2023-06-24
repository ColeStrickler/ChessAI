from board import Board
import pygame as p

BOARD_WIDTH = 60*8 + 200
BOARD_HEIGHT = 60*8


p.init()
screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
clock = p.time.Clock()
b = Board(p, screen)




while True:
    b.draw_Board()
   # b.get_Moves()



    for e in p.event.get():
        if e.type == p.QUIT:
            break
        elif e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos()
            b.select(location)





    clock.tick(15)
    p.display.flip()

