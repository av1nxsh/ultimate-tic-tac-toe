from typing import Dict, Any

""" board class: --> checking win
                 --> playing the game
                 --> returning board value and state
                 --> giving rewards
                 --> saving previous moves
                 
    player class:--> check next move
                    --> dict with past states and corresponding values
                 
"""

import numpy as np


def getHash(boards):
    hash_board = str(boards.reshape(9))
    return hash_board


class board:
    def __init__(self, computer, human):
        self.board = np.zeros((3, 3))
        self.hash = None
        self.end = False
        self.computer = computer
        self.human = human
        self.moves = []

    def gethash(self):
        self.hash = str(self.board.reshape(9))
        return self.hash

    def getmoves(self):
        moves = []
        for x, i in enumerate(self.board):
            for y, j in enumerate(i):
                if j == 0:
                    moves.append((x, y))
        return moves

    def getwin(self):
        """
        COMPUTER RESULTS
        ongoing = false
        # win = 1
        # loss = -1
        # draw = 0
        """

        sign = ''
        if not self.end:
            """checking row"""
            for x, row in enumerate(self.board):
                if row[0] == row[1] == row[2] != 0:
                    sign = row[0]
                    self.end = True

            """checking col"""
            temp_board = self.board.T.copy()
            for x, col in enumerate(temp_board):
                if col[0] == col[1] == col[2] != 0:
                    sign = col[0]
                    self.end = True

            """checking diagonals"""
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
                sign = self.board[1][1]
                self.end = True
            if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
                sign = self.board[1][1]
                self.end = True

            """checking for draw"""
            if self.getmoves() is None:
                sign = 0
                self.end = True

        if not self.end:
            return False
        if self.end:
            return 1 if sign == self.computer.sign else -1

    def giverewards(self, p):
        winner = self.getwin()
        if winner:
            if winner == 1:
                pass
            elif winner == 0:
                pass
            elif winner == -1:
                pass

    def makemove(self, p):
        move = p.bestmove(self.board)
        self.board[move] = p.sign

    def showBoard(self):
        # p1: x  p2: o
        token = ''
        for i in range(0, 3):
            print('-------------')
            out = '| '
            for j in range(0, 3):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

    def start(self):
        while not self.end:
            self.makemove(self.computer)
            self.showBoard()
            self.getwin()
            new_hash = self.gethash()
            self.moves.append(new_hash)
            self.makemove(self.human)
            self.getwin()
            self.showBoard()


class player:

    def __init__(self, sign=1):
        self.sign = sign
        self.board_score = {}

    def bestmove(self, current_board, ep=0.3):
        moves = current_board.getmoves()
        move = None
        explore = np.random.uniform(0, 1) < ep
        if explore:
            move = moves[(np.random.randint(0, len(moves)))]
        else:
            max_reward = -10
            for m in moves:
                new_board = current_board.copy()
                new_board[m] = 1
                hash_str = str(new_board.reshape(9))
                if self.board_score.get(hash_str) is None:
                    reward = 0
                else:
                    reward = self.board_score.get(hash_str)
                if max_reward < reward:
                    max_reward = reward
                    move = m
        current_board[move] = self.sign
        return move

computer = player(1)
human = player(-1)

board = board(computer, human)
board.start()