import sys

from board import Board
import threading
import pygame as p

BOARD_WIDTH = 60*8 + 200
BOARD_HEIGHT = 60*8

p.init()
screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
clock = p.time.Clock()
b = Board(p, screen)
p.display.set_caption("Chess")

AI_MOVE_LOCK = threading.Lock()
AI_THINKING_LOCK = threading.Lock()


def ai_moveThread():
    if b.white_turn and not b.ai_thinking:
        if AI_THINKING_LOCK.acquire(blocking=False):
            print("got lock")
            b.setAIThinking()
            AI_MAKE_MOVE_THREAD = threading.Thread(target=b.AI_MakeMove, args=())
            AI_MAKE_MOVE_THREAD.start()
            AI_THINKING_LOCK.release()
            print("released lock")






def GameLoop():
    b.draw_Board()
    ai_moveThread()

    for e in p.event.get():
        if e.type == p.QUIT:
            break
        elif e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos()
            b.select(location)

    clock.tick(15)
    p.display.flip()



while True:
    GameLoop()
