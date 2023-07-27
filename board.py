import copy
import itertools
import sys

from ai import ResolveMovesKing, ResolveMovesKnight, ResolveMovesQueen, ResolveMovesBishop, ResolveMovesPawn, ResolveMovesRook
import math
import time
import random

import numpy as np
import pygame as p
from pieces import Pawn, Knight, King, Rook, Queen, Bishop
from ai import AI

class Board():
    settings_width = 200
    entities = []
    turn = False
    c1 = (227, 213, 179)
    c2 = (194, 147, 29)
    select_c3 = (255, 255, 0, 128)
    sq_size = 60
    piece_lookup = {}
    selected = None

    check = False
    ai_thinking = False




    white_turn = True
    white_captured = []
    white_moves = {}
    whiteKing_Location = ()



    black_moves = {}
    black_captured = []
    blackKing_Location = ()

    def __init__(self, pyg, screen):
        self.pygame = pyg
        self.screen = screen
        self.setting_font = self.pygame.font.SysFont('Times New Roman', 25)
        self.message_font = self.pygame.font.SysFont('Times New Roman', 15)

        self.board = [["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]

        """
        TEST BOARD
        
        good board for testing checkmate
        
        
        
        
        
        self.board = [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["bR", "bR", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "wK", "  ", "  ", "  ", "  ", "  "]]
        self.board = [["wR", "  ", "wB", "wQ", "wK", "wB", "wN", "wR"],
                      ["wp", "wp", "wp", "wp", "  ", "wp", "wp", "wp"],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "wN", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["bp", "bp", "  ", "  ", "bp", "bp", "bp", "bp"],
                      ["bR", "bN", "bB", "  ", "bK", "bB", "bN", "bR"]]
        
        self.board = [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["wR", "wR", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "bK", "  ", "  ", "  ", "  ", "  "]]
        
        """

        self.ai = AI(self, search_depth=6)
        self.text_location = (self.screen.get_width() - self.settings_width + 15, self.screen.get_height() - 150)
        self.loading_texts = ["AI is thinking", "AI is thinking.", "AI is thinking..", "AI is thinking...", "AI is thinking...."]
        self.loading_texts_index = 0



        # Spawn piece entities
        for i in range(8):
            for j in range(8):
                pos = self.board[i][j]
                if pos == "  ":
                    continue
                else:
                    if pos[1] == "p":
                        e = Pawn(i, j, pos[0], self, self.screen)
                        self.piece_lookup[(i, j)] = e
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
                        self.set_KingLocation(pos[0], (i, j))

        self.checkGameState()


    """
    AI CONTROL WRAPPERS
    
    
    Need to add the Game Over check again
    """
    def AI_MakeMove(self):

        while True:
            piece_loc, move = self.ai.MakeMove()
            piece = self.piece_lookup[piece_loc]
            if piece.move(move):
                self.white_turn = not self.white_turn
                self.checkGameOver()
                self.setAIThinking()
                break
            #else:
                #print("ai failed")







    """
    GAME STATE FUNCTIONS
    """

    def setAIThinking(self):
        self.ai_thinking = not self.ai_thinking


    def SimMovePiece(self, board, src, src_val, tgt, tgt_val):
        y,x = tgt
        sy,sx = src
        board[y][x] = tgt_val
        board[sy][sx] = src_val

    def set_KingLocation(self, team, pos):
        if team == "b":
            self.blackKing_Location = pos
        else:
            self.whiteKing_Location = pos

    def take_piece(self, attacker, tgt):
        piece = self.piece_lookup[tgt]
        self.entities.remove(piece)
        if attacker.team == "w":
            self.white_captured.append(piece)
        else:
            self.black_captured.append(piece)

    def getValidMoves(self):
        self.black_moves.clear()
        self.white_moves.clear()

        for e in self.entities:
            if e.team == "b":
                self.black_moves[e.pos] = e.getMoves()
            else:
                self.white_moves[e.pos] = e.getMoves()







    """

       checkMoveFilter() will do the following:
       1. See if the current player is currently in check
       2. If so, we test every one of our possible moves and see if it will get us out of check
       3. If it will we keep that move, if not we will discard it

       """

    def checkMoveFilter(self, board, curr_team, currMoves, enemy_team, enemyMoves, king_loc):
        keys = list(currMoves.keys())
        old_king_loc = copy.deepcopy(king_loc)
        for src in keys:
            src_y, src_x = src
            src_val = board[src_y][src_x]
            c_moves = copy.deepcopy(currMoves[src])
            for move in c_moves:
                tgt_y, tgt_x = move
                tgt_val = board[tgt_y][tgt_x]
                if (src_y, src_x) == king_loc:
                    # print("found")
                    king_loc = move
                self.SimMovePiece(board, src, "  ", move, src_val)
                m_dict, next_turnEnemyMoves = self.ai.getMoves(board, enemy_team, beam_search=False)
                if king_loc in next_turnEnemyMoves:
                    currMoves[src].remove(move)
                king_loc = old_king_loc
                self.SimMovePiece(board, move, tgt_val, src, src_val)
            if len(currMoves[src]) == 0:
                currMoves.pop(src)


    def checkGameState(self):
        self.getValidMoves()
        board = copy.deepcopy(self.board)
        black_moves, black_moves_list = self.ai.getMoves(board, "b", beam_search=False)
        board = copy.deepcopy(self.board)
        white_moves, white_moves_list = self.ai.getMoves(board, "w", beam_search=False)
        self.checkMoveFilter(board, "w", white_moves, "b", black_moves_list, self.whiteKing_Location)
        self.checkMoveFilter(board, "b", black_moves, "w", white_moves_list, self.blackKing_Location)
        self.white_moves = white_moves
        self.black_moves = black_moves
        return len(self.black_moves) == 0 or len(self.white_moves) == 0

    def checkGameOver(self):
        if self.checkGameState():
            if len(self.white_moves) == 0:
                print("BLACK WINS!")
                sys.exit()
            elif len(self.black_moves) == 0:
                print("WHITE WINS!")
                sys.exit()

    """
    User Control/GUI Functions
    """

    def select(self, pos):
        x, y = pos
        y = int((y - (y % self.sq_size)) / self.sq_size)
        x = int((x - (x % self.sq_size)) / self.sq_size)
        if self.selected is None:
            if (y, x) in self.piece_lookup:
                self.selected = (y, x)
        else:
            piece = self.piece_lookup[self.selected]
            if self.white_turn or piece.team == "w":
                self.selected = None
                return
            self.checkGameOver()
            if piece.move((y, x)):
                self.white_turn = not self.white_turn
                self.checkGameOver()
            self.selected = None

    """
    Graphics/Draw Functions
    """
    def drawAccessoryTexts(self):
        if self.ai_thinking:
            load_text = self.message_font.render(self.loading_texts[self.loading_texts_index], False, (0,0,0))
            self.loading_texts_index += 1
            self.loading_texts_index %= 4
            self.screen.blit(load_text, self.text_location)

    def drawSelected(self):
        if self.selected:
            y,x = self.selected
            y *= self.sq_size
            x *= self.sq_size
            selection_surface = self.pygame.Surface((self.sq_size, self.sq_size), self.pygame.SRCALPHA)
            selection_surface.fill(self.select_c3)
            self.screen.blit(selection_surface, (x,y))



    def draw_Board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    p.draw.rect(self.screen, self.c1, p.Rect(i * 60, j * 60, 60, 60))
                else:
                    p.draw.rect(self.screen, self.c2, p.Rect(i * 60, j * 60, 60, 60))
        self.drawSettings()
        self.drawSelected()
        self.drawAccessoryTexts()
        for e in self.entities:
            e.draw()

    def drawSettings(self):
        offset_x = self.sq_size * 8
        self.pygame.draw.rect(self.screen, self.pygame.Color("gray"),
                              self.pygame.Rect(offset_x, 0, self.settings_width, self.sq_size * 8))
        white_pt_label = self.setting_font.render('White:', False, (0, 0, 0))
        black_pt_label = self.setting_font.render('Black:', False, (0, 0, 0))
        self.screen.blit(white_pt_label, (offset_x + 10, (self.sq_size * 8) / 8))
        self.screen.blit(black_pt_label, (offset_x + 10, ((self.sq_size * 8) / 6) * 3))

        offset_x = offset_x + 10
        offset_y = ((self.sq_size * 8) / 8) + 25
        num_printed = 0
        for p in self.white_captured:
            p.draw_icon(offset_x, offset_y)
            offset_x += 20
            num_printed += 1
            if num_printed > 7:
                offset_y += 20
                offset_x = self.sq_size * 8
                offset_x = offset_x + 10
                num_printed = 0

        offset_x = self.sq_size * 8
        offset_x = offset_x + 10
        offset_y = ((self.sq_size * 8) / 6) * 3 + 25
        num_printed = 0
        for p in self.black_captured:
            p.draw_icon(offset_x, offset_y)
            offset_x += 20
            num_printed += 1
            if num_printed > 7:
                offset_y += 20
                offset_x = self.sq_size * 8
                offset_x = offset_x + 10
                num_printed = 0
        return
