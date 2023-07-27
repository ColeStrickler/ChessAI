import copy
import random
import sys
import threading
import time

import numpy as np
import pygame as p



def MoveEvalFunc(board, move, score_dict, enemy_moves):
    y, x = move
    score = 0
    team = board[y][x][0]
    type = board[y][x][1]
    if type == " ":
        return 0
    score += 0.1/(1 + abs(y - 4) + score_dict[type])   # middle board control heuristic -> makes AI more aggressive
    return score_dict[type] + score

def OrderMoves(available_moves, board, score_dict, enemy_moves):
    if len(available_moves):
        available_moves.sort(key=lambda x: MoveEvalFunc(board, x, score_dict, enemy_moves), reverse=True)
        return available_moves
    return []

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
        if start and board[pos[0] + d1[0][1]][pos[1] + d1[0][0]] == "  ":
            d1.append((0, -2))
    else:
        d1 = [(0, 1)]
        d2 = [(-1, 1), (1, 1)]
        if start and board[pos[0] + d1[0][1]][pos[1] + d1[0][0]] == "  ":
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

def ResolveMovesKing(board, pos, f=False):
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
    def __init__(self, board, search_depth=6, team="w"):
        self.board = board
        self.strategy = 1               # Initial Strategy is Game Tree Search


        '''
        Evaluation settings
        '''
        self.w_moves = []
        self.b_moves = []

        """
        Alpha/Beta Search Options
        """
        self.ABSearch_Depth = search_depth
        self.maximizer_team = team
        if team == "w":
            self.minimizer_team = "b"
        else:
            self.minimizer_team = "w"
        self.chosen_move = ()
        self.thread_lock = threading.Lock()
        self.ab_lock = threading.Lock()
        self.best_SearchTreeMoves = []
        self.depth_beta = {0: 99999, 1:99999, 2:99999, 3:99999,4:99999,5:99999,6:99999,7:99999,8:99999,9:99999}
        self.depth_alpha = {0: -99999, 1:-99999, 2:-99999, 3:-99999,4:-99999,5:-99999,6:-99999,7:-99999,8:-99999,9:-99999}
        self.depth_alphac = {0: -99999, 1:-99999, 2:-99999, 3:-99999,4:-99999,5:-99999,6:-99999,7:-99999,8:-99999,9:-99999}
        self.depth_betac = {0: 99999, 1:99999, 2:99999, 3:99999,4:99999,5:99999,6:99999,7:99999,8:99999,9:99999}
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
    def ResolveMoves(self, board, pos, enemy_moves, beam_search=True):
        y,x = pos
        team = board[y][x][0]
        enemy_team = ""
        if team == "w":
            enemy_team = "b"
        else:
            enemy_team = "w"
        type = board[y][x][1]



        if beam_search:
            if type == "p":
                return OrderMoves(ResolveMovesPawn(board, pos), board, self.scoreDict, enemy_moves)#[0:1]
            elif type == "R":
                return OrderMoves(ResolveMovesRook(board, pos), board, self.scoreDict,enemy_moves)#[0:3]
            elif type == "N":
                return OrderMoves(ResolveMovesKnight(board, pos), board, self.scoreDict, enemy_moves)#[0:2]
            elif type == "B":
                return OrderMoves(ResolveMovesBishop(board, pos), board, self.scoreDict, enemy_moves)#[0:3]
            elif type == "Q":
                return OrderMoves(ResolveMovesQueen(board, pos), board, self.scoreDict, enemy_moves)#[0:3]
            elif type == "K":
                m = OrderMoves(ResolveMovesKing(board, pos), board, self.scoreDict, enemy_moves)#[0:5]
                return m
        else:
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


    def getMoves(self, board, team, beam_search=True):
        moves_dict = {}
        moves_list = []
        e_moves = []
        if beam_search == True:
            if team == "w":
                _, e_moves = self.getMoves(board, "b", beam_search=False)
            else:
                _, e_moves = self.getMoves(board, "w", beam_search=False)


        for m in range(len(board)):
            for n in range(len(board[0])):
                if board[m][n] != "  " and board[m][n][0] == team:
                    moves = self.ResolveMoves(board, (m,n), e_moves, beam_search=beam_search)
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

        return self.AB_Search(-99999, 99999, depth=0, threaded=True)

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
    def AB_Search(self, alpha, beta, depth, threaded=True):
        board, white_king_loc, black_king_loc = self.GetAB_Board()
        start_time = time.time()
        if threaded:
            chosen_piece, chosen_move = self.ABSearch_Thread(board, white_king_loc, black_king_loc, [])
        else:
            utility, chosen_piece, chosen_move = self.AB_Max(alpha, beta, board, depth, white_king_loc, black_king_loc, [])

        end_time = time.time()
        elapsed_time = end_time - start_time

        print("Elapsed time:", elapsed_time, "seconds", f"{chosen_piece}->{chosen_move}")
        return (chosen_piece, chosen_move)

    """
    
    checkMoveFilter() will do the following:
    1. See if the current player is currently in check
    2. If so, we test every one of our possible moves and see if it will get us out of check
    3. If it will we keep that move, if not we will discard it
    
    """
    def checkMoveFilter(self, board, curr_team, currMoves, enemy_team, enemyMoves, king_loc):
        keys = list(currMoves.keys())
        if king_loc in enemyMoves:
            for src in keys:
                src_y, src_x = src
                src_val = board[src_y][src_x]
                c_moves = copy.deepcopy(currMoves[src])
                for move in c_moves:
                    tgt_y, tgt_x = move
                    tgt_val = board[tgt_y][tgt_x]
                    old_king_loc = king_loc
                    if (src_y, src_x) == king_loc:
                        king_loc = move
                    self.SimMovePiece(board, src, "  ", move, src_val)
                    m_dict, next_turnEnemyMoves = self.getMoves(board, enemy_team)
                    if king_loc in next_turnEnemyMoves:
                        currMoves[src].remove(move)
                        if len(currMoves[src]) == 0:
                            currMoves.pop(src)
                    king_loc = old_king_loc
                    self.SimMovePiece(board, move, tgt_val, src, src_val)


    '''
    This function is a multi-threaded implementation of beam search
    '''
    def ABSearch_Thread(self, board, wk_Loc, bk_Loc, prev_movList):
        moves_dict, moves_list = self.getMoves(board, self.maximizer_team)
        self.checkMoveFilter(board, self.maximizer_team, moves_dict, self.minimizer_team, prev_movList, wk_Loc)
        if len(moves_dict) == 0:
            return (self.evaluateBoard(board, True, self.minimizer_team), (), ())
        threads = []
        bk_Store = ()
        i = 0
        move = {}
        '''
        store moves and their corresponding indexes in this structure
        we will pass in the index as a tag that will get appended to self.best_SearchTreeMoves
        after we sort for the best utility in self.best_SearchTreeMoves, we use its tag to access the best move from move = {}
        '''
        for piece in moves_dict:
            piece_val = board[piece[0]][piece[1]]
            new_board = copy.deepcopy(board)
            self.ab_lock.acquire()
            ab_max_thread = threading.Thread(target=self.AB_Max, args=(-99999, 99999, new_board, 0, wk_Loc, bk_Loc, [], i, {piece: moves_dict[piece]}, True))
            threads.append(ab_max_thread)
            ab_max_thread.start()
            self.ab_lock.release()
            move[i] = (piece, p)
            i += 1
        for thread in threads:
            thread.join()
        self.best_SearchTreeMoves.sort(key=lambda x: x[0], reverse=True)
        best = self.best_SearchTreeMoves[0]
        #print(self.best_SearchTreeMoves)
        self.best_SearchTreeMoves.clear()
        self.depth_alpha = self.depth_alphac
        self.depth_beta = self.depth_betac
        return best[1], best[2]



    """
    Heuristic Search maximizer function
    """
    def AB_Max(self, alpha, beta, board, depth, wk_Loc, bk_Loc, prev_movList, tag=None, piece_dict=None, threaded=False):
        if depth == self.ABSearch_Depth:
            return (self.evaluateBoard(board, False, self.maximizer_team), (), ())
        moves_dict, moves_list = self.getMoves(board, self.maximizer_team)
        if depth == 0 and threaded:
            moves_dict = piece_dict
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
                utility, cp, cm = self.AB_Min(alpha, beta, board, depth + 1, wk_Loc, bk_Loc, moves_dict, threaded=threaded)
                """ALPHA BETA PRUNING"""
                alpha = max(alpha, utility)
                if not threaded:
                    if utility > utility_max:
                        utility_max = utility
                        chosen_move = p
                        chosen_piece = piece
                    if beta <= alpha:
                        self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
                        break
                else:
                    if utility > utility_max:
                        utility_max = utility
                        chosen_move = p
                        chosen_piece = piece
                    self.ab_lock.acquire()
                    self.depth_alpha[depth] = max(self.depth_alpha[depth], alpha)
                    if self.depth_beta[depth] <= alpha or self.depth_beta[depth] <= self.depth_alpha[depth] or alpha <= beta:
                        self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
                        self.ab_lock.release()
                        #print(f"pruning {depth}")
                        break
                    self.ab_lock.release()
                """ALPHA BETA PRUNING"""

                if piece == bk_Store:
                    bk_Loc = bk_Store

                self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
            if beta <= alpha:
                break

        if depth == 0:
            self.thread_lock.acquire()
            self.best_SearchTreeMoves.append((utility_max, chosen_piece, chosen_move))
            self.thread_lock.release()
        return utility_max, chosen_piece, chosen_move

    """
    Heuristic Search minimizer function
    """
    def AB_Min(self, alpha, beta, board, depth, wk_Loc, bk_Loc, prev_movList, threaded=False):
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
                utility, cp, cm = self.AB_Max(alpha, beta, board, depth + 1, wk_Loc, bk_Loc, moves_dict, threaded=threaded)
                """ALPHA BETA PRUNING"""
                beta = min(utility, beta)
                if not threaded:
                    if utility < utility_min:
                        utility_min = utility
                        chosen_move = p
                        chosen_piece = piece
                    if beta <= alpha:
                        self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
                        break
                else:
                    if utility < utility_min:
                        utility_min = utility
                        chosen_move = p
                        chosen_piece = piece
                    self.ab_lock.acquire()
                    self.depth_beta[depth] = min(self.depth_beta[depth], beta)
                    if beta <= self.depth_alpha[depth] or self.depth_beta[depth] <= self.depth_alpha[depth] or alpha <= beta:
                        self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
                        self.ab_lock.release()
                       # print(f"pruning {depth}")
                        break
                    self.ab_lock.release()
                """ALPHA BETA PRUNING"""

                if piece == wk_Store:
                    wk_Loc = wk_Store

                self.SimMovePiece(board, p, src_val=old_val, tgt=piece, tgt_val=piece_val)
            if beta <= alpha:
                break
        return utility_min, chosen_piece, chosen_move

