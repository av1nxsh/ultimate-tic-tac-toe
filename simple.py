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
import time


def getHash(boards):
    hash_board = str(boards.reshape(9))
    return hash_board


class board:
    def __init__(self, computer, human):
        self.board = np.zeros((3, 3))
        """self.board = [
            [1, -1, 1],
            [-1, 1, 1],
            [1, -1, 0]
        ]"""
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
        # draw = 0.5
        """

        sign = ''
        moves = self.getmoves()
        if not self.end:
            """checking row"""
            for x, row in enumerate(self.board):
                if sum(row) == 3:
                    self.end = True
                    return 1
                if sum(row) == -3:
                    self.end = True
                    return 1


            """checking col"""
            temp_board = self.board.T.copy()
            for x, col in enumerate(temp_board):
                if sum(col) == 3:
                    self.end = True
                    return 1
                if sum(col) == -3:
                    self.end = True
                    return 1
            """checking diagonals"""
            if self.board[0][0] + self.board[1][1] + self.board[2][2] == 3:
                self.end = True
                return 1
            if self.board[0][0] + self.board[1][1] + self.board[2][2] == -3:
                self.end = True
                return -1
            if self.board[0][2] + self.board[1][1] + self.board[2][0] == 3:
                self.end = True
                return 1
            if self.board[0][2] + self.board[1][1] + self.board[2][0] == -3:
                self.end = True
                return -1

            """checking for draw"""
            if not moves:
                self.end = True
                return 0.5

        if not self.end:
            return False



    def makemove(self, p):
        move = p.bestmove(self)
        if move:
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

    def giverewards(self, comp):
        winner = self.getwin()
        for h in self.moves:
            comp.rewards(h, winner)
            # give rewards

    def start(self):
        for i in range(10):
            while not self.end:
                self.showBoard()
                new_hash = self.gethash()
                print(new_hash)
                self.makemove(self.computer)
                self.showBoard()
                new_hash = self.gethash()
                print(new_hash)
                win = self.getwin()
                if win:
                    if win != 0.5:
                        print(win)
                    else:
                        print(0)
                    break
                new_hash = self.gethash()
                self.moves.append(new_hash)
                self.makemove(self.human)
                self.getwin()
                win = self.getwin()
                if win:
                    print(win)
                    print()


class player:

    def __init__(self, sign=1):
        self.sign = sign
        self.board_score = {}

    def bestmove(self, boards, ep=0.3):
        current_board = boards.board.copy()
        moves = boards.getmoves()
        move = None
        explore = np.random.uniform(0, 1) < ep
        if explore and len(moves) != 0:
            move = moves[(np.random.randint(0, len(moves)))]
        else:
            max_reward = -10
            if len(moves) != 0:
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

    def gethash(self, board):
        hash_board = str(board.reshape(9))
        return hash_board

    def rewards(self, hash_str, reward):
        al = 0.4  # alpha value
        df = 0.3  # discount factor
        if self.board_score.get(hash_str) is None:
            self.board_score[hash_str] = 0
        self.board_score[hash_str] += al * (reward + self.board_score[hash_str] * (df + 1))


computer = player(1)
human = player(-1)

board = board(computer, human)
board.start()