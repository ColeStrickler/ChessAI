import copy
import random

import pygame as p



def ResolveMovesPawn(board, pos):
    y, x = pos
    team = board[y][x][0]
    start = (team == "w" and y == 1) or (team == "b" and y == 6)
    d1 = []
    d2 = []
    available_moves = []
    if team == "b":
        d1 = [(0, -1)]
        d2 = [(1, -1), (-1, -1)]
        if start:
            d1.append((0, -2))
    else:
        d1 = [(0, 1)]
        d2 = [(-1, 1), (1, 1)]
        if start:
            d1.append((0, 2))

    for d in d1:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y
        if m < 8 and n < 8 and m >= 0 and n >= 0 and board[m][n] == "  ":
            available_moves.append((m, n))
    for d in d2:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y
        if m < 8 and n < 8 and m >= 0 and n >= 0 and board[m][n][0] != team and board[m][n] != "  ":
            available_moves.append((m, n))

    return available_moves

def ResolveMovesRook(board, pos):
    dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    available_moves = []
    y, x = pos
    team = board[y][x][0]
    for d in dir:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y
        while m < 8 and n < 8 and m >= 0 and n >= 0 and board[m][n] == "  ":
            available_moves.append((m, n))
            n += x
            m += y
        if m < 8 and n < 8 and m >= 0 and n >= 0:
            if board[m][n][0] != team:
                available_moves.append((m, n))
    return available_moves

def ResolveMovesKnight(board, pos):
    y, x = pos
    team = board[y][x][0]
    dir = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]
    available_moves = []
    for d in dir:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y
        if m < 8 and n < 8 and m >= 0 and n >= 0 and (board[m][n] == "  " or board[m][n][0] != team):
            available_moves.append((m, n))
    return available_moves

def ResolveMovesBishop(board, pos):
    y, x = pos
    team = board[y][x][0]
    dir = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    available_moves = []
    for d in dir:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y

        while m < 8 and n < 8 and m >= 0 and n >= 0 and board[m][n] == "  ":
            available_moves.append((m, n))
            n += x
            m += y
        if m < 8 and n < 8 and m >= 0 and n >= 0:
            if board[m][n][0] != team:
                available_moves.append((m, n))
    return available_moves

def ResolveMovesQueen(board, pos):
    y, x = pos
    team = board[y][x][0]
    dir = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    available_moves = []
    for d in dir:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y
        while m < 8 and n < 8 and m >= 0 and n >= 0 and board[m][n] == "  ":
            available_moves.append((m, n))
            n += x
            m += y
        if m < 8 and n < 8 and m >= 0 and n >= 0:
            if board[m][n][0] != team:
                available_moves.append((m, n))
    return available_moves

def ResolveMovesKing(board, pos):
    y, x = pos
    team = board[y][x][0]
    dir = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    available_moves = []
    for d in dir:
        x, y = d
        n = pos[1] + x
        m = pos[0] + y
        if m < 8 and n < 8 and m >= 0 and n >= 0 and (board[m][n] == "  " or board[m][n][0] != team):
            available_moves.append((m, n))
    return available_moves



def ResolveMoves(board, pos):
    y,x = pos
    team = board[y][x][0]
    type = board[y][x][1]

    if type == "p":
        return ResolveMovesPawn(board, pos)
    elif type == "R":
        return ResolveMovesRook(board, pos)
    elif type == "N":
        return ResolveMovesKnight(board, pos)
    elif type == "B":
        return ResolveMovesBishop(board, pos)
    elif type == "Q":
        return ResolveMovesQueen(board, pos)
    elif type == "K":
        return ResolveMovesKing(board, pos)







class AI():
    def __init__(self, board):
        self.board = board
        self.strategy = 1               # Initial Strategy is Game Tree Search


        """
        Alpha/Beta Search Options
        """
        self.ABSearch_Depth = 4
        self.maximizer_team = "w"
        self.minimizer_team = "b"


        """
        State Evaluation Hyperparameters
        """
        self.king_val =     1000
        self.queen_val =    8
        self.rook_val =     5
        self.bishop_val =   5
        self.knight_val =   3
        self.pawn_val =     1


    def getMoves(self, board, team):
        moves_dict = {}
        #print(board)
        for m in range(len(board)):
            for n in range(len(board[0])):
                if board[m][n] != "  " and board[m][n][0] == team:
                    moves_dict[(m,n)] = ResolveMoves(board, (m,n))


        return moves_dict


    def MakeMove(self):
        if self.strategy == 1:
            return self.GameTreeSearch()



    def GameTreeSearch(self):
        move = ((),())
        """
        This method is a variation of Heuristic Alpha-Beta Tree Search.
        Our variation of the algorithm includes:
        1. Transposition Tables -> Avoid some repeated computation
        2. Cutoff Search -> We specify a depth limited cutoff
        3. Beam Search -> We only consider n best moves
        4. Pieces are valued during state evaluation based on total weight
        """
        best = -9999

        board = copy.deepcopy(self.board.board)
        moves_dict = self.getMoves(board, self.maximizer_team)
        choice = random.choice(list(moves_dict))
        while len(moves_dict[choice]) == 0:
            choice = random.choice(list(moves_dict))
        #print(choice)

        return (choice, moves_dict[choice][0])





        for move in self.moves:
            start_alpha = 0
            start_beta = 0
            best_found = self.AB_Search(start_alpha, start_beta, depth=0)



        return move


    def AB_Search(self, alpha, beta, depth, score):

        board = copy.deepcopy(self.board.board)

        return self.AB_Max(alpha, beta, board, depth, score)

    def AB_Max(self, alpha, beta, board, depth):

        self.AB_Min(alpha, beta, board, depth + 1)

    def AB_Min(self, alpha, beta, board, depth):
        self.AB_Max(alpha, beta, board, depth + 1)