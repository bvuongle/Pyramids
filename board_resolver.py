from board import Board
from hints import HintsData
from condition_analysis import CondBoard


class BoardResolver():
    def __init__(self, hints=HintsData(), condBrd=CondBoard()):
        self.flag = 0
        self._curBrd = Board(dim=hints.dim)
        self._curBrd.fillBoardWithValue(0)
        self._hints = hints
        self._condBrd = condBrd

    @property
    def curBrd(self):
        return self._curBrd

    @curBrd.setter
    def curBrd(self, newBoard: Board()):
        self._curBrd = newBoard
        return self._curBrd

    def renewCurBrd(self):
        self._curBrd = Board(dim=self.hints.dim)
        self._curBrd.fillBoardWithValue(0)

    @property
    def hints(self):
        return self._hints

    @hints.setter
    def hints(self, newHints: HintsData):
        self._hints = newHints
        return self._hints

    @property
    def condBrd(self):
        return self._condBrd

    @condBrd.setter
    def condBrd(self, newCondBrd: CondBoard()):
        self._condBrd = newCondBrd
        return self._condBrd

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
        f = open(dir, 'w')
        f.write("Answer to the problem with board size of ")
        f.write(f"N = {self.hints.dim}, and hints is as follows: ")
        f.write("\n[\n")
        f.writelines(f"{x} " for x in self.hints.topHint)
        f.write("\n")
        f.writelines(f"{x} " for x in self.hints.botHint)
        f.write("\n")
        f.writelines(f"{x} " for x in self.hints.rightHint)
        f.write("\n")
        f.writelines(f"{x} " for x in self.hints.leftHint)
        f.write("\n]\n\n")
        f.write("#"*20)
        f.write("\n")
        for row in self.curBrd.board:
            for cell in row:
                f.write(f"{cell} ")
            f.write("\n")
        f.write("#"*20)
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
