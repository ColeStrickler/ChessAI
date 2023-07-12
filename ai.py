import copy
import random
import sys

import numpy as np
import pygame as p



def MoveEvalFunc(board, move, score_dict):
    y, x = move
    team = board[y][x][0]
    type = board[y][x][1]
    if type == " ":
        return 0
    return score_dict[type]


"""
CUTTING OUT ONLY THE TOP FIVE MOVES --> EXPERIMENTAL
"""
def OrderMoves(available_moves, board, score_dict):
    available_moves.sort(key=lambda x: MoveEvalFunc(board, x, score_dict), reverse=True)
    return available_moves

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

def ResolveMoves(board, pos, score_dict):
    y,x = pos
    team = board[y][x][0]
    type = board[y][x][1]

    if type == "p":
        return OrderMoves(ResolveMovesPawn(board, pos), board, score_dict)[0:1]
    elif type == "R":
        return OrderMoves(ResolveMovesRook(board, pos), board, score_dict)[0:3]
    elif type == "N":
        return OrderMoves(ResolveMovesKnight(board, pos), board, score_dict)[0:2]
    elif type == "B":
        return OrderMoves(ResolveMovesBishop(board, pos), board, score_dict)[0:3]
    elif type == "Q":
        return OrderMoves(ResolveMovesQueen(board, pos), board, score_dict)[0:3]
    elif type == "K":
        return OrderMoves(ResolveMovesKing(board, pos), board, score_dict)[0:5]

class AI():
    def __init__(self, board):
        self.board = board
        self.strategy = 1               # Initial Strategy is Game Tree Search


        """
        Alpha/Beta Search Options
        """
        self.ABSearch_Depth = 6
        self.maximizer_team = "w"
        self.minimizer_team = "b"
        self.counter = 0


        """
        State Evaluation Hyperparameters
        """
        self.king_val =     9
        self.queen_val =    8
        self.rook_val =     5
        self.bishop_val =   5
        self.knight_val =   3
        self.pawn_val =     1
        self.scoreDict = {}
        self.scoreDict["K"] = self.king_val
        self.scoreDict["N"] = self.knight_val
        self.scoreDict["p"] = self.pawn_val
        self.scoreDict["R"] = self.rook_val
        self.scoreDict["Q"] = self.queen_val
        self.scoreDict["B"] = self.bishop_val



    def getMoves(self, board, team):
        moves_dict = {}
        #print(board)
        for m in range(len(board)):
            for n in range(len(board[0])):
                if board[m][n] != "  " and board[m][n][0] == team:
                    moves_dict[(m,n)] = ResolveMoves(board, (m,n), self.scoreDict)

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

        return self.AB_Search(-99999, 99999, depth=0)


    def evaluateBoard(self, board):
        score = 0
        found = 0
        for m in range(len(board)):
            for n in range(len(board[0])):
                if board[m][n] != '  ':
                    team = board[m][n][0]
                    type = board[m][n][1]
                    if team == self.minimizer_team:
                        score -= self.getScore(board[m][n])
                    else:
                        score += self.getScore(board[m][n])
                        found += 1
        return score


    def getScore(self, tgt):
        type = tgt[1]
        return self.scoreDict[type]






    """
    Alpha = Max bound, Beta = Min Bound
    """


    def AB_Search(self, alpha, beta, depth):
        board = copy.deepcopy(self.board.board)
        utility, chosen_piece, chosen_move = self.AB_Max(alpha, beta, board, depth)
        print(f"FINAL {chosen_piece}->{chosen_move} UTILITY: {utility}")
        return (chosen_piece, chosen_move)


    def SimMovePiece(self, board, src, src_val, tgt, tgt_val):
        y,x = tgt
        sy,sx = src
        board[y][x] = tgt_val
        board[sy][sx] = src_val



    def AB_Max(self, alpha, beta, board, depth):
        if depth == self.ABSearch_Depth:
            return (self.evaluateBoard(board), (), ())
        moves_dict = self.getMoves(board, self.maximizer_team)
        utility_max = -999999
        chosen_move = ()
        chosen_piece = ()
        for piece in moves_dict:
            for p in moves_dict[piece]:
                piece_val = board[piece[0]][piece[1]]
                old_val = board[p[0]][p[1]]
                self.SimMovePiece(board=board, src=piece, src_val="  ", tgt=p, tgt_val=piece_val)
                utility, cp, cm = self.AB_Min(alpha, beta, board, depth + 1)

                """ALPHA BETA PRUNING"""
                alpha = max(alpha, utility)
                if utility > utility_max:
                    utility_max = utility
                    chosen_move = p
                    chosen_piece = piece
                if beta <= alpha:
                    self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
                    break
                """ALPHA BETA PRUNING"""
                self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
            if beta <= alpha:
                break
        return utility_max, chosen_piece, chosen_move



    def AB_Min(self, alpha, beta, board, depth):
        if depth == self.ABSearch_Depth:
            return (self.evaluateBoard(board), (), ())
        moves_dict = self.getMoves(board, self.minimizer_team)
        utility_min = 999999
        chosen_move = ()
        chosen_piece = ()
        for piece in moves_dict:
            for p in moves_dict[piece]:
                piece_val = board[piece[0]][piece[1]]
                old_val = board[p[0]][p[1]]
                self.SimMovePiece(board=board, src=piece, src_val="  ", tgt=p, tgt_val=piece_val)
                utility, cp, cm = self.AB_Max(alpha, beta, board, depth + 1)

                """ALPHA BETA PRUNING"""
                beta = min(utility, beta)
                if utility < utility_min:
                    utility_min = utility
                    chosen_move = p
                    chosen_piece = piece
                if beta <= alpha:
                    self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
                    break
                """ALPHA BETA PRUNING"""
                self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
            if beta <= alpha:
                break
        return utility_min, chosen_piece, chosen_move

