import pygame as p
import numpy as np


"""
PIECE CLASSES --> ONLY USED INTERNAL TO THE BOARD CLASS
"""



"""
SWITCH MOVES IN BOARD TO USING A DICTIONARY FORMAT, IT IS MUCH BETTER THAN THE CURRENT


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
        try:
            if self.team == "w":
                if tgt not in self.board.white_moves[self.pos]:
                    return False
            else:
                if tgt not in self.board.black_moves[self.pos]:
                    return False
        except Exception as e:
            print(f"exception: {e} self.team: {self.team}, {self.pos}")
            return False

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

    def getBestCaptured(self):
        best = "  "
        best_score = 0
        if self.team == "w":
            for cp in self.board.black_captured:
                score = self.board.ai.getScore(cp.team + cp.type)
                if score > best_score:
                    best = cp
                    best_score = 0
        else:
            for cp in self.board.white_captured:
                score = self.board.ai.getScore(cp.team + cp.type)
                if score > best_score:
                    best = cp
                    best_score = 0
        return best

    def replace_White(self):
        replacement = self.getBestCaptured()
        replacement.pos = self.pos
        self.board.black_captured.remove(replacement)
        self.board.black_captured.append(self)
        self.board.entities.remove(self)
        self.board.entities.append(replacement)

    def replace_Black(self):
        replacement = self.getBestCaptured()
        replacement.pos = self.pos
        self.board.white_captured.remove(replacement)
        self.board.white_captured.append(self)
        self.board.entities.remove(self)
        self.board.entities.append(replacement)

    def checkUpgrade(self):
        if self.team == "w" and self.pos[0] == 7:
            self.replace_White()
        elif self.team == "b" and self.pos[0] == 0:
            self.replace_Black()



    def getMoves(self):
        d1 = []
        d2 = []
        self.available_moves.clear()
        if self.direction == 1:
            d1 = [(0, -1)]
            d2 = [(1,-1), (-1, -1)]
            if self.start and self.board.board[self.pos[0] + d1[0][1]][self.pos[1] + d1[0][0]] == "  ":
                d1.append((0, -2))
        else:
            d1 = [(0, 1)]
            d2 = [(-1, 1), (1, 1)]
            if self.start and self.board.board[self.pos[0] + d1[0][1]][self.pos[1] + d1[0][0]] == "  ":
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
        try:
            if self.team == "w":
                if tgt not in self.board.white_moves[self.pos]:
                    return False
            else:
                if tgt not in self.board.black_moves[self.pos]:
                    return False
        except Exception as e:
            return False

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
            self.checkUpgrade()
            return True
        else:
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

            if m < 8 and n < 8 and m >= 0 and n >= 0 and (self.board.board[m][n] == "  " or self.board.board[m][n][0] != self.team):
                self.available_moves.append((m, n))
        #print(self.available_moves)
        return self.available_moves

    def setKingLocation(self):
        if self.team == "b":
            self.board.blackKing_Location = self.pos
        else:
            self.board.whiteKing_Location = self.pos


    def move(self, tgt):
        try:
            if self.team == "w":
                if tgt not in self.board.white_moves[self.pos]:
                    return False
            else:
                if tgt not in self.board.black_moves[self.pos]:
                    return False
        except Exception as e:
            return False
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


