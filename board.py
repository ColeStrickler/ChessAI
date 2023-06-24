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
    sq_size = 60
    piece_lookup = {}
    selected = None
    white_turn = True
    white_captured = []
    black_captured = []


    def __init__(self, pyg, screen):
        self.pygame = pyg
        self.screen = screen

        self.board = [["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "bp", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]

        # Spawn piece entities
        for i in range(8):
            for j in range(8):
                pos = self.board[i][j]
                if pos == "  ":
                    continue
                else:
                    if pos[1] == "p":
                        e = Pawn(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i,j)] = e
                        self.entities.append(e)
                    elif pos[1] == "R":
                        e = Rook(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i, j)] = e
                        self.entities.append(e)
                    elif pos[1] == "N":
                        e = Knight(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i, j)] = e
                        self.entities.append(e)
                    elif pos[1] == "B":
                        e = Bishop(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i, j)] = e
                        self.entities.append(e)
                    elif pos[1] == "Q":
                        e = Queen(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i, j)] = e
                        self.entities.append(e)
                    elif pos[1] == "K":
                        e = King(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i, j)] = e
                        self.entities.append(e)


    def draw_Board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    p.draw.rect(self.screen, self.c1, p.Rect(i*60, j*60, 60, 60))
                else:
                    p.draw.rect(self.screen, self.c2, p.Rect(i * 60, j * 60, 60, 60))

        for e in self.entities:
            e.draw()


    def select(self, pos):
        x, y = pos
        y = int((y - (y % self.sq_size)) / self.sq_size)
        x = int((x - (x % self.sq_size)) / self.sq_size)
        if self.selected is None:
            if (y,x) in self.piece_lookup:
                self.selected = (y,x)
        else:
            piece = self.piece_lookup[self.selected]
            if (self.white_turn and piece.team != "w") or (not self.white_turn and piece.team != "b"):
                self.selected = None
                return
            print(f"selected: {piece}")
            piece.move((y, x))
            self.selected = None
            self.white_turn = not self.white_turn

    def take_piece(self, attacker, tgt):
        piece = self.piece_lookup[tgt]
        self.entities.remove(piece)
        if attacker.team == "w":
            self.white_captured.append(piece)
        else:
            self.black_captured.append(piece)
            print(self.black_captured)


    def get_Moves(self):
        for e in self.entities:
            if e.type == "B":
                 e.getMoves()
        return