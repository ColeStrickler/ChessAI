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
        self.king_val =     10
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

    """
    Move retrieval and Evaluation Functions
    
    NOTE: Beam Search is implemented within ResolveMoves()
    """
    def ResolveMoves(self, board, pos):
        y,x = pos
        team = board[y][x][0]
        type = board[y][x][1]

        if type == "p":
            return OrderMoves(ResolveMovesPawn(board, pos), board, self.scoreDict)[0:1]
        elif type == "R":
            return OrderMoves(ResolveMovesRook(board, pos), board, self.scoreDict)
        elif type == "N":
            return OrderMoves(ResolveMovesKnight(board, pos), board, self.scoreDict)[0:2]
        elif type == "B":
            return OrderMoves(ResolveMovesBishop(board, pos), board, self.scoreDict)[0:3]
        elif type == "Q":
            return OrderMoves(ResolveMovesQueen(board, pos), board, self.scoreDict)[0:3]
        elif type == "K":
            return OrderMoves(ResolveMovesKing(board, pos), board, self.scoreDict)[0:5]

    def getMoves(self, board, team):
        moves_dict = {}
        moves_list = []
        for m in range(len(board)):
            for n in range(len(board[0])):
                if board[m][n] != "  " and board[m][n][0] == team:
                    moves = self.ResolveMoves(board, (m,n))
                    moves_dict[(m,n)] = moves
                    moves_list += moves
        return moves_dict, moves_list

    def MakeMove(self):
        if self.strategy == 1:
            return self.GameTreeSearch()

    def SimMovePiece(self, board, src, src_val, tgt, tgt_val):
        y,x = tgt
        sy,sx = src
        board[y][x] = tgt_val
        board[sy][sx] = src_val

    """
    Heuristic Evaluation Functions
    """
    def evaluateBoard(self, board, checkmate, team):
        if checkmate:
            if team == self.maximizer_team:
                return 100
            else:
                return -100
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

    """
    Wrapper function for retrieving scores
    """
    def getScore(self, tgt):
        type = tgt[1]
        return self.scoreDict[type]

    """
    Heuristic Alpha-Beta Minimax
    """
    def GameTreeSearch(self):
        move = ((),())
        """
        This method is a variation of Heuristic Alpha-Beta Tree Search.
        Our variation of the algorithm includes:
        1. Transposition Tables -> Avoid some repeated computation
        2. Cutoff Search -> We specify a depth limited cutoff
        3. Beam Search -> We only consider n best moves
        4. Pieces are valued during state evaluation based on total weight
        
        
        Alpha = Max bound, Beta = Min Bound
        """
        best = -9999

        return self.AB_Search(-99999, 99999, depth=0)

    """
    GetAB_Board is a helper/wrapper function that retrieves some info used in the heuristic search tree
    """
    def GetAB_Board(self):
        board = copy.deepcopy(self.board.board)
        return board, self.board.whiteKing_Location, self.board.blackKing_Location


    """
    This is a wrapper function that will format the result of the heuristic search into a format acceptable
    by the board.AI_MakeMove() function
    """
    def AB_Search(self, alpha, beta, depth):
        board, white_king_loc, black_king_loc = self.GetAB_Board()
        utility, chosen_piece, chosen_move = self.AB_Max(alpha, beta, board, depth, white_king_loc, black_king_loc, [])
        return (chosen_piece, chosen_move)

    """
    
    checkMoveFilter() will do the following:
    1. See if the current player is currently in check
    2. If so, we test every one of our possible moves and see if it will get us out of check
    3. If it will we keep that move, if not we will discard it
    
    """
    def checkMoveFilter(self, board, curr_team, currMoves, enemy_team, enemyMoves, king_loc):
        if king_loc in enemyMoves:
            for src in currMoves.keys():
                src_y, src_x = src
                src_val = board[src_y][src_x]
                for move in currMoves[src]:
                    tgt_y, tgt_x = move
                    tgt_val = board[tgt_y][tgt_x]
                    self.SimMovePiece(board, src, "  ", move, src_val)
                    m_dict, next_turnEnemyMoves = self.getMoves(board, enemy_team)
                    if king_loc in next_turnEnemyMoves:
                        currMoves[src].remove(move)
                        if len(currMoves[src]) == 0:
                            currMoves.pop(src)
                    self.SimMovePiece(board, move, tgt_val, src, src_val)


    """
    Heuristic Search maximizer function
    """
    def AB_Max(self, alpha, beta, board, depth, wk_Loc, bk_Loc, prev_movList):
        if depth == self.ABSearch_Depth:
            return (self.evaluateBoard(board, False, self.maximizer_team), (), ())
        moves_dict, moves_list = self.getMoves(board, self.maximizer_team)
        self.checkMoveFilter(board, self.maximizer_team, moves_dict, self.minimizer_team, prev_movList, wk_Loc)
        if len(moves_dict) == 0:
            return (self.evaluateBoard(board, True, self.minimizer_team), (), ())
        utility_max = -999999
        chosen_move = ()
        chosen_piece = ()
        bk_Store = ()

        for piece in moves_dict:
            piece_val = board[piece[0]][piece[1]]
            for p in moves_dict[piece]:
                old_val = board[p[0]][p[1]]

                if piece == bk_Loc:
                    bk_Store = bk_Loc
                    bk_Loc = p

                self.SimMovePiece(board=board, src=piece, src_val="  ", tgt=p, tgt_val=piece_val)
                utility, cp, cm = self.AB_Min(alpha, beta, board, depth + 1, wk_Loc, bk_Loc, moves_dict)

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

                if piece == bk_Store:
                    bk_Loc = bk_Store

                self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
            if beta <= alpha:
                break
        return utility_max, chosen_piece, chosen_move

    """
    Heuristic Search minimizer function
    """
    def AB_Min(self, alpha, beta, board, depth, wk_Loc, bk_Loc, prev_movList):
        if depth == self.ABSearch_Depth:
            return (self.evaluateBoard(board, False, self.minimizer_team), (), ())
        moves_dict, moves_list = self.getMoves(board, self.minimizer_team)
        self.checkMoveFilter(board, self.minimizer_team, moves_dict, self.maximizer_team, prev_movList, bk_Loc)
        if len(moves_dict) == 0:
            return (self.evaluateBoard(board, True, self.maximizer_team), (), ())


        utility_min = 999999
        chosen_move = ()
        chosen_piece = ()
        wk_Store = ()
        for piece in moves_dict:
            piece_val = board[piece[0]][piece[1]]
            for p in moves_dict[piece]:
                old_val = board[p[0]][p[1]]
                if piece == wk_Loc:
                    wk_Store = wk_Loc
                    wk_Loc = p
                self.SimMovePiece(board=board, src=piece, src_val="  ", tgt=p, tgt_val=piece_val)
                utility, cp, cm = self.AB_Max(alpha, beta, board, depth + 1, wk_Loc, bk_Loc, moves_dict)

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

                if piece == wk_Store:
                    wk_Loc = wk_Store

                self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
            if beta <= alpha:
                break
        return utility_min, chosen_piece, chosen_move

