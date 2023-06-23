import pygame as p

class Pawn():
    upgraded = False
    type = "p"
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (x, y)
        self.team = team
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + "p.png"), self.board.sq_size)


    def draw(self):
        rect = p.Rect(self.pos[0] * self.board.sq_size[0], self.pos[1] * self.board.sq_size[0], self.board.sq_size[0], self.board.sq_size[1])
        self.screen.blit(self.image, rect)



class Knight():
    upgraded = False
    type = "N"
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (x, y)
        self.team = team
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + "N.png"), self.board.sq_size)


    def draw(self):
        rect = p.Rect(self.pos[0] * self.board.sq_size[0], self.pos[1] * self.board.sq_size[0], self.board.sq_size[0], self.board.sq_size[1])
        self.screen.blit(self.image, rect)


class King():
    upgraded = False
    type = "K"
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (x, y)
        self.team = team
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + "K.png"), self.board.sq_size)


    def draw(self):
        rect = p.Rect(self.pos[0] * self.board.sq_size[0], self.pos[1] * self.board.sq_size[0], self.board.sq_size[0], self.board.sq_size[1])
        self.screen.blit(self.image, rect)


class Rook():
    upgraded = False
    type = "R"
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (x, y)
        self.team = team
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + "R.png"), self.board.sq_size)


    def draw(self):
        rect = p.Rect(self.pos[0] * self.board.sq_size[0], self.pos[1] * self.board.sq_size[0], self.board.sq_size[0], self.board.sq_size[1])
        self.screen.blit(self.image, rect)



class Queen():
    upgraded = False
    type = "Q"
    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (x, y)
        self.team = team
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + "Q.png"), self.board.sq_size)


    def draw(self):
        rect = p.Rect(self.pos[0] * self.board.sq_size[0], self.pos[1] * self.board.sq_size[0], self.board.sq_size[0], self.board.sq_size[1])
        self.screen.blit(self.image, rect)


class Bishop():
    upgraded = False
    available_moves = []
    type = "B"

    def __init__(self, y, x, team, board, screen):
        self.board = board
        self.screen = screen
        self.pos = (x, y)
        self.team = team
        self.start = True
        self.image = p.transform.scale(p.image.load("assets/" + self.team + "B.png"), self.board.sq_size)


    def draw(self):
        rect = p.Rect(self.pos[0] * self.board.sq_size[0], self.pos[1] * self.board.sq_size[0], self.board.sq_size[0], self.board.sq_size[1])
        self.screen.blit(self.image, rect)


    def getMoves(self):
        dir = [(1,1), (1,-1), (-1,1), (-1,-1)]
        self.available_moves.clear()
        for d in dir:
            y = d[0]
            x = d[1]
            n = self.pos[0] + x
            m = self.pos[1] + y
            while m < 8 and n < 8 and m >= 0 and n >= 0 and self.board.board[m][n] == "  ":
                self.available_moves.append((m, n))
                n += x
                m += y

            if m < 8 and n < 8 and m >= 0 and n >= 0:
                if self.board.board[m][n][0] != self.team:
                    self.available_moves.append((m, n))
                    print(self.available_moves)
        #print(self.available_moves)
        return self.available_moves


