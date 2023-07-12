import pygame as p
import numpy as np


"""
PIECE CLASSES --> ONLY USED INTERNAL TO THE BOARD CLASS
"""

class Piece():
    type = ""
    image = None
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (y, x)
        self.team = team
        self.icon_size = 25
        self.icon = None
        self.available_moves = []

    def moveValid(self, move):
        if self.team == "b":
            if move in self.board.black_moves:
                return True
        else:
            if move in self.board.white_moves:
                return True

    def move(self, tgt):
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
            return True
        else:
            return False


    def override_move(self, tgt):
        y,x = self.pos
        ret = None
        self.board.board[y][x] = "  "
        if self.pos in self.board.piece_lookup:
            self.board.piece_lookup.pop(self.pos)
        if tgt in self.board.piece_lookup:
            ret = self.board.piece_lookup[tgt]
            self.board.entities.remove(ret)
        self.board.piece_lookup[tgt] = self
        self.pos = tgt
        y, x = self.pos
        self.board.board[y][x] = f"{self.team}{self.type}"
        self.start = False
        self.getMoves()
        return ret

    def getMoves(self):
        return

    def draw(self):
        rect = p.Rect(self.pos[1] * self.board.sq_size, self.pos[0] * self.board.sq_size, self.board.sq_size, self.board.sq_size)
        self.screen.blit(self.image, rect)

    def draw_icon(self, x, y):
        rect = p.Rect(x, y, self.icon_size, self.icon_size)
        self.screen.blit(self.icon, rect)


class Pawn(Piece):
    upgraded = False
    type = "p"

    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        self.icon = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.icon_size, self.icon_size))
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
        else:
            d1 = [(0, 1)]
            d2 = [(-1, 1), (1, 1)]
            if self.start:
                d1.append((0, 2))

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
            if m < 8 and n < 8 and m >= 0 and n >= 0 and self.board.board[m][n][0] != self.team and self.board.board[m][n] != "  ":
                self.available_moves.append((m, n))

        return self.available_moves


    def move(self, tgt):
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
            self.start = False
            return True
        else:
            print("not in available moves")
            return False


class Knight(Piece):
    type = "N"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        self.icon = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.icon_size, self.icon_size))

    def getMoves(self):
        dir = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
        self.available_moves.clear()
        for d in dir:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            if m < 8 and n < 8 and m >= 0 and n >= 0 and (self.board.board[m][n] == "  " or self.board.board[m][n][0] != self.team):
                self.available_moves.append((m, n))
        return self.available_moves


class King(Piece):
    type = "K"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        self.icon = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"),(self.icon_size, self.icon_size))

    def getMoves(self):
        dir = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        self.available_moves.clear()
        for d in dir:
            x, y = d
            n = self.pos[1] + x
            m = self.pos[0] + y
            if self.team == "w":
                if (m,n) in self.board.black_moves:
                    continue
            else:
                if (m,n) in self.board.white_moves:
                    continue



            if m < 8 and n < 8 and m >= 0 and n >= 0 and (self.board.board[m][n] == "  " or self.board.board[m][n][0] != self.team):
                self.available_moves.append((m, n))
        return self.available_moves

    def setKingLocation(self):
        if self.team == "b":
            self.board.blackKing_Location = self.pos
        else:
            self.board.whiteKing_Location = self.pos

    def override_move(self, tgt):
        y,x = self.pos
        ret = False
        self.board.board[y][x] = "  "
        if self.pos in self.board.piece_lookup:
            self.board.piece_lookup.pop(self.pos)
        if tgt in self.board.piece_lookup:
            ret = self.board.piece_lookup[tgt]
            self.board.entities.remove(ret)
        self.board.piece_lookup[tgt] = self
        self.pos = tgt
        y, x = self.pos
        self.board.board[y][x] = f"{self.team}{self.type}"
        self.start = False
        self.setKingLocation()
        self.getMoves()
        return ret

    def move(self, tgt):
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
            self.setKingLocation()
            return True
        else:
            return False


class Rook(Piece):
    type = "R"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        self.icon = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.icon_size, self.icon_size))
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
        return self.available_moves


class Queen(Piece):
    type = "Q"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        self.icon = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.icon_size, self.icon_size))

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
        return self.available_moves



class Bishop(Piece):
    type = "B"
    def __init__(self, y, x, team, board, screen):
        super().__init__(y, x, team, board, screen)
        self.image = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.board.sq_size, self.board.sq_size))
        self.icon = p.transform.scale(p.image.load("assets/" + self.team + f"{self.type}.png"), (self.icon_size, self.icon_size))

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
            return self.available_moves


