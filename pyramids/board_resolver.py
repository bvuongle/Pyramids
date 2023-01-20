from board import Board
from hints import HintsData
from condition_analysis import CondBoard
from exception import NoSolutionError


class BoardResolver():
    """BoardResolver class stores the data of a problem, including the
    input data: hints, the condition board and the problem results
    (if it's exist). It also includes methods that are used as tools
    to solve the problem from input data.
    """
    def __init__(self, hints=HintsData()):
        self._flag = 0
        self._curBrd = Board(dim=hints.dim)
        self._curBrd.fillBoardWithValue(0)
        self._hints = hints
        self._condBrd = CondBoard(dim=hints.dim)

    @property
    def flag(self):
        """This flag marks if the current object is storing the
        configuration as the solution of the problem or not.
        If flag is 0, then no solution has been found yet, and vice
        versa if flag is 1

        :return: value of flag
        :rtype: int
        """
        return self._flag

    @flag.setter
    def flag(self, value: int):
        self._flag = value
        return self._flag

    @property
    def curBrd(self):
        """Current configuration of the board for the problem.
        By default, all cells in the board have a value of 0. If flag = 1,
        then this property is the answer to the problem.

        :return: Current configuration of the board
        :rtype: Board
        """
        return self._curBrd

    @property
    def condBrd(self):
        """Condition board is created for the problem

        :return: condition board
        :rtype: CondBoard
        """
        return self._condBrd

    @property
    def hints(self):
        """Input data of the problem - hints

        :return: list of lists of hints :)
        :rtype: HintsData
        """
        return self._hints

    @hints.setter
    def hints(self, newHints):
        self._hints = newHints
        return self._hints

    @staticmethod
    def getRow(matrix, row) -> list:
        """Returns a list of the current value of the specified row in a matrix

        :param matrix: Matrix for which we need to take the value
        :type matrix: list
        :param row: Row in the matrix that we need to get the value
        :type row: int
        :return: List of values in current row of the matrix
        :rtype: list
        """
        return [x for x in matrix[row] if x != 0]

    @staticmethod
    def getCol(matrix, col) -> list:
        """Returns a list of the current value of the specified column
        in a matrix

        :param matrix: Matrix for which we need to take the value
        :type matrix: list
        :param col: Column in the matrix that we need to get the value
        :type col: int
        :return: List of values in current column of the matrix
        :rtype: list
        """
        return [row[col] for row in matrix if row[col] != 0]

    @staticmethod
    def numVisiblePyramids(arr) -> int:
        """Calculates the length of the longest incremented sequence
        that starts with the first element of the array.\n
        Used to calculate how many pyramids can be seen at the
        specified location.

        :return: the length of the longest incremented sequence
        :rtype: int
        """
        cur = arr[0]
        n = len(arr)
        cnt = 1
        for i in range(1, n):
            if arr[i] > cur:
                cnt += 1
                cur = arr[i]
        return cnt

    def saveData(self, dir):
        """Store the result of the problem in a file if flag = 1
        (found the answer)

        :param dir: the path to the file where answer will be saved
        :type dir: str
        :raises FileNotFoundError: exception - directory is empty
        """
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
        """Check if the current configuration of the object is satisfied with
        the input condition.\n
        At each row/column, we will get the list of values of that row/column,
        calculate how many pyramids we can see with this configuration and
        compare it with the corresponding hint (if the hint is not 0).

        :return: Is the answer right or wrong?
        :rtype: bool
        """
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

    def backtracking(self, row: int, col: int):
        """Backtracking algorithm, where the problem is solved.
        This algorithm will generate all possible configurations of the board
        (based on the condition board and the values that have already been
        placed in the board) until it finds a match.

        :param row: current row that the algorithm considers
        :type row: int
        :param col: current column that the algorithm considers
        :type col: int
        """
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
        """Method prepares the condition table and calls
        the method to solve the problem.

        :raises NoSolutionError: exception - can't find the solution
        """
        try:
            self.condBrd.analyzeBasicCond(self.hints)
        except NoSolutionError:
            raise NoSolutionError()
        self.backtracking(0, 0)
        if self.flag == 0:
            raise NoSolutionError()
