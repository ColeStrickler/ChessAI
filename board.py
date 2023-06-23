import math
import time
import random
import pygame as p
from pieces import Pawn, Knight, King, Rook, Queen, Bishop

class Board():
    entities = []
    turn = False
    c1 = (227, 213, 179)
    c2 = (194, 147, 29)
    sq_size = (60, 60)


    def __init__(self, pyg, screen):
        self.pygame = pyg
        self.screen = screen

        self.board = [["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]

        # Spawn piece entities
        for i in range(8):
            for j in range(8):
                pos = self.board[i][j]
                if pos[1] == "p":
                    self.entities.append(Pawn(i, j, pos[0], self, self.screen))
                elif pos[1] == "R":
                    self.entities.append(Rook(i, j, pos[0], self, self.screen))
                elif pos[1] == "N":
                    self.entities.append(Knight(i, j, pos[0], self, self.screen))
                elif pos[1] == "B":
                    self.entities.append(Bishop(i, j, pos[0], self, self.screen))
                elif pos[1] == "Q":
                    self.entities.append(Queen(i, j, pos[0], self, self.screen))
                elif pos[1] == "K":
                    self.entities.append(King(i, j, pos[0], self, self.screen))


    def draw_Board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    p.draw.rect(self.screen, self.c1, p.Rect(i*60, j*60, 60, 60))
                else:
                    p.draw.rect(self.screen, self.c2, p.Rect(i * 60, j * 60, 60, 60))

        for e in self.entities:
            e.draw()


    def get_Moves(self):
        for e in self.entities:
            if e.type == "B":
                 print(e.team, e.getMoves())
        return