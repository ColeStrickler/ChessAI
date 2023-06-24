from board import Board
import pygame as p


p.init()
screen = p.display.set_mode((60*8, 60*8))
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

