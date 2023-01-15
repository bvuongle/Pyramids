from board import Board
from hints import HintsData
from exception import NoSolutionError


class CondBoard(Board):
    def __init__(self, dim=0, board=[], base=[]):
        super().__init__(dim, board)
        self.fillBoardWithValue(base)

    @staticmethod
    def noSolutionCheck(hint: list):
        cnt_H_min = cnt_H_max = 0
        for amount in hint:
            if amount == 1:
                cnt_H_min += 1
            elif amount == len(hint):
                cnt_H_max += 1
        return cnt_H_min <= 1 and cnt_H_max <= 1

    def setNdelValueCol(self, row, col, value) -> None:
        # Set this value for cell at (row, column)
        # and remove it from cell's list in the same column
        self.board[row][col] = [value]
        for otrCol in range(self.dim):
            if otrCol != col and value in self.board[row][otrCol]:
                self.board[row][otrCol].remove(value)
        return None

    def setNdelValueRow(self, row, col, value) -> None:
        # Set this value for cell at (row, column)
        # and remove it from cell's list in the same row
        self.board[row][col] = [value]
        for otrRow in range(self.dim):
            if otrRow != row and value in self.board[otrRow][col]:
                self.board[otrRow][col].remove(value)
        return None

    def topCond(self, topHint: list) -> None:
        # Remember that you should loop col from 0 -> N-1, row = 0
        if not self.noSolutionCheck(topHint):
            raise NoSolutionError
        for col, amount in enumerate(topHint):
            if amount == 0:
                continue
            elif amount == 1:
                self.setNdelValueCol(0, col, self.dim)
                self.setNdelValueRow(0, col, self.dim)
            elif amount == self.dim:
                for row in range(self.dim):
                    self.setNdelValueCol(row, col, row+1)
            else:
                self.board[0][col] = self.board[0][col][:self.dim-amount+1]
                for otrRow in range(1, amount-1):
                    if self.dim in self.board[otrRow][col]:
                        self.board[otrRow][col].remove(self.dim)
        return None

    def botCond(self, botHint: list) -> None:
        # Remember that you should loop col from N-1 -> 0, row = N-1
        if not self.noSolutionCheck(botHint):
            raise NoSolutionError
        for col, amount in enumerate(botHint):
            if amount == 0:
                continue
            elif amount == 1:
                self.setNdelValueCol(self.dim-1, col, self.dim)
                self.setNdelValueRow(self.dim-1, col, self.dim)
            elif amount == self.dim:
                for row in range(self.dim):
                    self.setNdelValueCol(row, col, self.dim-row)
            else:
                self.board[self.dim-1][col] = \
                    self.board[self.dim-1][col][:self.dim-amount+1]
                for otrRow in range(self.dim-amount+1, self.dim-1):
                    if self.dim in self.board[otrRow][col]:
                        self.board[otrRow][col].remove(self.dim)
        return None

    def rightCond(self, rightHint: list) -> None:
        # Remember that you should loop row from 0 -> N-1, col = 0
        if not self.noSolutionCheck(rightHint):
            raise NoSolutionError
        for row, amount in enumerate(rightHint):
            if amount == 0:
                continue
            elif amount == 0:
                continue
            if amount == 1:
                self.setNdelValueRow(row, 0, self.dim)
                self.setNdelValueCol(row, 0, self.dim)
            elif amount == self.dim:
                for col in range(self.dim):
                    self.setNdelValueRow(row, col, col+1)
            else:
                self.board[row][0] = self.board[row][0][:self.dim-amount+1]
                for otrCol in range(1, amount-1):
                    if self.dim in self.board[row][otrCol]:
                        self.board[row][otrCol].remove(self.dim)
        return None

    def leftCond(self, leftHint: list) -> None:
        # Remember that you should loop row from N-1 -> 0, col = N-1
        if not self.noSolutionCheck(leftHint):
            raise NoSolutionError
        for row, amount in enumerate(leftHint):
            if amount == 0:
                continue
            elif amount == 1:
                self.setNdelValueRow(row, self.dim-1, self.dim)
                self.setNdelValueCol(row, self.dim-1, self.dim)
            elif amount == self.dim:
                for col in range(self.dim):
                    self.setNdelValueRow(row, col, self.dim-col)
            else:
                self.board[row][self.dim-1] = \
                    self.board[row][self.dim-1][:self.dim-amount+1]
                for otrCol in range(self.dim-amount+1, self.dim-1):
                    if self.dim in self.board[row][otrCol]:
                        self.board[row][otrCol].remove(self.dim)
        return self

    def remRedundantCond(self) -> None:
        for row in range(self.dim):
            for col in range(self.dim):
                if len(self.board[row][col]) == 1:
                    self.setNdelValueCol(row, col, self.board[row][col][0])
                    self.setNdelValueRow(row, col, self.board[row][col][0])
        return None

    def analyzeBasicCond(self, hints: HintsData) -> None:
        self.topCond(hints.topHint)
        self.botCond(hints.botHint)
        self.rightCond(hints.rightHint)
        self.leftCond(hints.leftHint)
        self.remRedundantCond()
        return None