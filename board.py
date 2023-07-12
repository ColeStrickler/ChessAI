import copy
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
    sq_size = 60
    piece_lookup = {}
    selected = None

    check = False

    white_turn = True
    white_captured = []
    white_moves = []
    whiteKing_Location = ()



    black_moves = []
    black_captured = []
    blackKing_Location = ()

    def __init__(self, pyg, screen):
        self.pygame = pyg
        self.screen = screen
        self.setting_font = self.pygame.font.SysFont('Times New Roman', 25)
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
        self.board = [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["wR", "wR", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
                      ["  ", "  ", "bR", "  ", "  ", "  ", "  ", "  "]]
        
        
        """

        self.ai = AI(self)






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
    """
    def AI_MakeMove(self):
        piece_loc, move = self.ai.MakeMove()
        piece = self.piece_lookup[piece_loc]
        #print(f"AI Selected {piece} --> {move}")


        if piece.move(move):
            self.white_turn = not self.white_turn
            self.checkGameOver()






    """
    GAME STATE FUNCTIONS
    """

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
                self.black_moves += e.getMoves()
            else:
                self.white_moves += e.getMoves()

    def isCheck(self):
        if self.whiteKing_Location in self.black_moves or self.blackKing_Location in self.white_moves:
            self.check = True
        else:
            self.check = False
        return self.check



    def ValidOOC_Moves(self, entity):
        """
           This method will test a move to see if it gets the player out of check. This method is used to filter out invalid
           moves during a state of check inside the method call checkGameState().
        """
        valid_moves = []
        for m in entity.available_moves:
            backtrack = entity.pos
            placeback_entity = entity.override_move(m)
            self.getValidMoves()
            if not self.isCheck():
                valid_moves.append(m)
            entity.override_move(backtrack)
            if placeback_entity:  # if we captured an entity, place it back
                self.entities.append(placeback_entity)
                placeback_entity.override_move(m)
                placeback_entity.getMoves()
        return valid_moves

    def checkGameState(self):
        self.getValidMoves()
        if self.isCheck():
            if self.white_turn:
                valid_moves = []
                for e in self.entities:
                    if e.team == "w":
                        valid_moves += self.ValidOOC_Moves(e)
                self.white_moves = valid_moves
                return len(self.white_moves) == 0
            else:
                valid_moves = []
                for e in self.entities:
                    self.getValidMoves()
                    if e.team == "b":
                        valid_moves += self.ValidOOC_Moves(e)
                self.getValidMoves()
                self.black_moves = valid_moves
                return len(self.black_moves) == 0
        return False


    def checkGameOver(self):
        if self.checkGameState():
            if self.white_turn:
                print("BLACK WINS!")
            else:
                print("WHITE WINS!")


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



            if self.white_turn:
                if (y,x) not in self.white_moves:
                    return False
            else:
                if (y,x) not in self.black_moves:
                    return False


            if piece.move((y, x)):
                self.white_turn = not self.white_turn
                self.checkGameOver()
            self.selected = None

    """
    Graphics/Draw Functions
    """

    def draw_Board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    p.draw.rect(self.screen, self.c1, p.Rect(i * 60, j * 60, 60, 60))
                else:
                    p.draw.rect(self.screen, self.c2, p.Rect(i * 60, j * 60, 60, 60))
        self.drawSettings()
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
