from board import Board
from hints import HintsData


class noSolutionError(Exception):
    def __init__(self):
        super().__init__("This problem have no solution")


class CondBoard(Board):
    def __init__(self, base: list, dim=0, board=[]):
        super().__init__(dim, board)
        self.fillBoardWithValue(base)

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
        if not noSolutionCheck(topHint):
            raise noSolutionError
        for col, amount in enumerate(topHint):
            if amount == 0:
                continue
            elif amount == 1:
                self.setNdelValueCol(0, col, self.dim)
                self.setNdelValueRow(0, col, self.dim)
            elif amount == self.dim:
                for row in range(self.dim):
                    self.setNdelValueCol(row, col, row+1)
            # else:
            #     pyramidMatrix[0][col] = pyramidMatrix[0][col][:N-amount+1]
            #     for otrRow in range(1, amount):
            #         if N in pyramidMatrix[otrRow][col]:
            #             pyramidMatrix[otrRow][col].remove(N)
        return None

    def botCond(self, botHint: list) -> None:
        # Remember that you should loop col from N-1 -> 0, row = N-1
        if not noSolutionCheck(botHint):
            raise noSolutionError
        for col, amount in enumerate(botHint):
            if amount == 0:
                continue
            elif amount == 1:
                self.setNdelValueCol(self.dim-1, col, self.dim)
                self.setNdelValueRow(self.dim-1, col, self.dim)
            elif amount == self.dim:
                for row in range(self.dim):
                    self.setNdelValueCol(row, col, self.dim-row)
            # else:
            #     pyramidMatrix[N-1][col] = pyramidMatrix[N-1][col][:N-amount+1]
            #     for otrRow in range(N-amount+1, N-1):
            #         if N in pyramidMatrix[otrRow][col]:
            #             pyramidMatrix[otrRow][col].remove(N)
        return None

    def rightCond(self, rightHint: list) -> None:
        # Remember that you should loop row from 0 -> N-1, col = 0
        if not noSolutionCheck(rightHint):
            raise noSolutionError
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
            # else:
            #     pyramidMatrix[row][0] = pyramidMatrix[row][0][:N-amount+1]
            #     for otrCol in range(1, amount):
            #         if N in pyramidMatrix[row][otrCol]:
            #             pyramidMatrix[row][otrCol].remove(N)
        return None

    def leftCond(self, leftHint: list) -> None:
        # Remember that you should loop row from N-1 -> 0, col = N-1
        if not noSolutionCheck(leftHint):
            raise noSolutionError
        for row, amount in enumerate(leftHint):
            if amount == 0:
                continue
            elif amount == 1:
                self.setNdelValueRow(row, self.dim-1, self.dim)
                self.setNdelValueCol(row, self.dim-1, self.dim)
            elif amount == self.dim:
                for col in range(self.dim):
                    self.setNdelValueRow(row, col, self.dim-col)
            # else:
            #     pyramidMatrix[row][N-1] = pyramidMatrix[row][N-1][:N-amount+1]
            #     for otrCol in range(N-amount+1, N-1):
            #         if N in pyramidMatrix[row][otrCol]:
            #             pyramidMatrix[row][otrCol].remove(N)
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


def noSolutionCheck(hint: list):
    cnt_H_min = cnt_H_max = 0
    for amount in hint:
        if amount == 1:
            cnt_H_min += 1
        elif amount == len(hint):
            cnt_H_max += 1
    return cnt_H_min <= 1 and cnt_H_max <= 1
