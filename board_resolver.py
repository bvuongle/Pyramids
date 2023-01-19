from board import Board
from hints import HintsData
from condition_analysis import CondBoard
from exception import NoSolutionError


class BoardResolver():
    def __init__(self, hints=HintsData()):
        self.flag = 0
        self._curBrd = Board(dim=hints.dim)
        self._curBrd.fillBoardWithValue(0)
        self._hints = hints
        self._condBrd = CondBoard(dim=hints.dim)

    @property
    def curBrd(self):
        return self._curBrd

    @property
    def condBrd(self):
        return self._condBrd

    @property
    def hints(self):
        return self._hints

    @hints.setter
    def hints(self, newHints):
        self._hints = newHints
        return self._hints

    @staticmethod
    def getRow(matrix, row) -> list:
        return [x for x in matrix[row] if x != 0]

    @staticmethod
    def getCol(matrix, col) -> list:
        return [row[col] for row in matrix if row[col] != 0]

    @staticmethod
    def numVisiblePyramids(arr) -> int:
        cur = arr[0]
        n = len(arr)
        cnt = 1
        for i in range(1, n):
            if arr[i] > cur:
                cnt += 1
                cur = arr[i]
        return cnt

    def saveData(self, dir):
        if self.flag == 0:
            return None
        try:
            f = open(dir, 'w')
        except FileNotFoundError:
            raise FileNotFoundError()
        answer = "Answer to the problem with board size of "\
            + f"N = {self.hints.dim}, and hints is as follows: "\
            + "\n[\n"\
            + " ".join([str(x) for x in self.hints.topHint]) + "\n"\
            + " ".join([str(x) for x in self.hints.botHint]) + "\n"\
            + " ".join([str(x) for x in self.hints.rightHint]) + "\n"\
            + " ".join([str(x) for x in self.hints.leftHint])\
            + "\n]\n\n" + "#"*20 + "\n"\
            + "\n".join(
                [" ".join([str(cell) for cell in row])
                 for row in self.curBrd.board])\
            + "\n" + "#"*20
        f.write(answer)
        f.close()

    def checkResultWithCond(self) -> bool:
        for idx in range(0, self.hints.dim):
            topCond = self.hints.topHint[idx]
            botCond = self.hints.botHint[idx]
            rightCond = self.hints.rightHint[idx]
            leftCond = self.hints.leftHint[idx]

            tmpRow = []
            for row in range(0, self.curBrd.dim):
                tmpRow.append(self.curBrd.board[row][idx])
            visibleTop = self.numVisiblePyramids(tmpRow)
            visibleBot = self.numVisiblePyramids(tmpRow[::-1])

            tmpCol = []
            for col in range(0, self.curBrd.dim):
                tmpCol.append(self.curBrd.board[idx][col])
            visibleRight = self.numVisiblePyramids(tmpCol)
            visibleLeft = self.numVisiblePyramids(tmpCol[::-1])

            if (visibleTop != topCond and topCond != 0) or \
                    (visibleBot != botCond and botCond != 0) or \
                    (visibleRight != rightCond and rightCond != 0) or \
                    (visibleLeft != leftCond and leftCond != 0):
                return False
            else:
                continue
        return True

    def backtracking(self, row, col):
        if row == self.curBrd.dim-1 and col > self.curBrd.dim-1:
            if self.checkResultWithCond():
                self.flag = 1
                return self.curBrd
            else:
                return None
        if row < self.curBrd.dim-1 and col > self.curBrd.dim-1:
            row += 1
            col = 0
        remSet = set(self.getRow(self.curBrd.board, row)).union(
            set(self.getCol(self.curBrd.board, col)))
        for value in range(1, self.curBrd.dim+1):
            if value in self.condBrd.board[row][col] and value not in remSet:
                self.curBrd.board[row][col] = value
                self.backtracking(row, col+1)
                if self.flag == 1:
                    return self.curBrd
                self.curBrd.board[row][col] = 0

    def resolver(self):
        try:
            self.condBrd.analyzeBasicCond(self.hints)
        except NoSolutionError:
            raise NoSolutionError()
        self.backtracking(0, 0)
        if self.flag == 0:
            raise NoSolutionError()
