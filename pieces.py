import pygame as p
import numpy as np


class Piece():
    available_moves = []
    type = ""
    image = None
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (y, x)
        self.team = team

    def move(self, tgt):
        self.getMoves()
        if tgt in self.available_moves:
            y,x = self.pos
            self.board.board[y][x] = "  "
            self.board.piece_lookup.pop(self.pos)
            if tgt in self.board.piece_lookup:
                self.board.take_piece(self, tgt)
            self.board.piece_lookup[tgt] = self
            self.pos = tgt
            y, x = self.pos
            self.board.board[y][x] = f"{self.team}{self.type}"

    def getMoves(self):
        return

    def draw(self):
        rect = p.Rect(self.pos[1] * self.board.sq_size, self.pos[0] * self.board.sq_size, self.board.sq_size, self.board.sq_size)
        self.screen.blit(self.image, rect)




class Pawn(Piece):
    upgraded = False
    type = "p"

    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        if self.team == "b":
            self.direction = 1
        else:
            self.direction = 0

    def getMoves(self):
        d1 = []
        d2 = []
        self.available_moves.clear()
        if self.direction == 1:
            d1 = [(0, -1)]
            d2 = [(1,-1), (-1, -1)]
            if self.start:
                d1.append((0, -2))
                self.start = False
        else:
            d1 = [(0, 1)]
            d2 = [(-1, 1), (1, 1)]
            if self.start:
                d1.append((0, 2))
                self.start = False

        for d in d1:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            if m < 8 and n < 8 and m >= 0 and n >= 0 and self.board.board[m][n] == "  ":
                self.available_moves.append((m, n))
        for d in d2:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            if self.board.board[m][n][0] != self.team and self.board.board[m][n] != "  ":
                self.available_moves.append((m, n))



class Knight(Piece):
    type = "N"

    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))

    def getMoves(self):
        dir = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
        self.available_moves.clear()
        for d in dir:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            if m < 8 and n < 8 and m >= 0 and n >= 0 and (self.board.board[m][n] == "  " or self.board.board[m][n][0] != self.team):
                self.available_moves.append((m, n))
        print(self.available_moves)

class King(Piece):
    type = "K"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))

    def getMoves(self):
        dir = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        self.available_moves.clear()
        for d in dir:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            if m < 8 and n < 8 and m >= 0 and n >= 0 and (self.board.board[m][n] == "  " or self.board.board[m][n][0] != self.team):
                self.available_moves.append((m, n))


class Rook(Piece):
    type = "R"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))

    def getMoves(self):
        dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.available_moves.clear()
        for d in dir:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            while m < 8 and n < 8 and m >= 0 and n >= 0 and self.board.board[m][n] == "  ":
                self.available_moves.append((m, n))
                n += x
                m += y
            if m < 8 and n < 8 and m >= 0 and n >= 0:
                if self.board.board[m][n][0] != self.team:
                    self.available_moves.append((m, n))


class Queen(Piece):
    type = "Q"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))

    def getMoves(self):
        dir = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        self.available_moves.clear()
        for d in dir:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            while m < 8 and n < 8 and m >= 0 and n >= 0 and self.board.board[m][n] == "  ":
                self.available_moves.append((m, n))
                n += x
                m += y
            if m < 8 and n < 8 and m >= 0 and n >= 0:
                if self.board.board[m][n][0] != self.team:
                    self.available_moves.append((m, n))



class Bishop(Piece):
    type = "B"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))

    def getMoves(self):
            dir = [(1,1), (1,-1), (-1,1), (-1,-1)]
            self.available_moves.clear()
            for d in dir:
                x,y = d
                n = self.pos[1] + x
                m = self.pos[0] + y

                while m < 8 and n < 8 and m >= 0 and n >= 0 and self.board.board[m][n] == "  ":
                    self.available_moves.append((m, n))
                    n += x
                    m += y
                if m < 8 and n < 8 and m >= 0 and n >= 0:
                    if self.board.board[m][n][0] != self.team:
                        self.available_moves.append((m, n))


