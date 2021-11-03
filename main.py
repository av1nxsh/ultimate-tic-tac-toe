import numpy as np
import matplotlib as plt


def checkwin(board):
    for row in board:
        if row.sum() == 3:
            return True
    for row in board.T:
        if row.sum() == 3:
            return True
    for i in range(3):
        add = board[i][i]
    if np.reshape(board, [-1])[::4].sum() == 3:
        return True
    if np.reshape(board, [-1])[2:7:2].sum() == 3:
        return True
    return False


class inside:
    def __init__(self, x, y):
        self.moves = []
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.x = x
        self.y = y

    def getmoves(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    self.moves.append((i, j))

    def move(self, player):
        self.getmoves()
        if player == 1:
            self.board[self.moves[0][0]][self.moves[0][1]] = 1
        else:
            self.board[self.moves[0][0]][self.moves[0][1]] = 0

    def printline(self, i):
        board = self.board
        for j in range(len(board[i])):
            mark = ' '
            if j == 0:
                print("| ", end="")
            if board[i][j] == 1:
                mark = 'X'
            elif board[i][j] == 2:
                mark = 'O'
            elif board[i][j] == 0:
                mark = '*'
            if j == len(board[i]) - 1:
                print(str(mark), end='  |  ')
            else:
                print(str(mark) + "|", end='')


class outside:
    shell = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    state = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def __init__(self):
        for i in range(len(self.shell)):
            for j in range(len(self.shell[i])):
                self.shell[i][j] = inside(i, j)

    def printbox(self):
        print("----------------------------------")
        for i in range(len(self.shell)):
            for k in range(3):
                for j in range(len(self.shell[i])):
                    self.shell[i][j].printline(k)
                print("")
            print("----------------------------------")

    def win(self):
        board = self.state
        for row in board:
            if row.sum() == 3:
                return True
        for row in board.T:
            if row.sum() == 3:
                return True
        for i in range(3):
            add = board[i][i]
        if np.reshape(board, [-1])[::4].sum() == 3:
            return True
        if np.reshape(board, [-1])[2:7:2].sum() == 3:
            return True
        return False


test = outside()
test.printbox()
