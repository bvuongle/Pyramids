from copy import deepcopy


class WrongDimension(Exception):
    def __init__(self) -> None:
        super().__init__("Dimension of this board is \
            different from the one provided")


class Board():
    def __init__(self, dim=0, board=[]):
        self.__checkDimNBoardRelation(dim, board)
        self._dim = dim if dim != 0 else len(board)
        self._board = board

    def __checkDimNBoardRelation(self, dim, board):
        if dim != 0 and board:
            if len(board) != dim:
                raise WrongDimension()

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, val):
        self._dim = val

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, lst):
        self._board = deepcopy(lst)

    def fillBoardWithValue(self, value):
        newBrd = []
        for _ in range(self._dim):
            rowList = []
            for _ in range(self._dim):
                rowList.append(deepcopy(value))
            newBrd.append(rowList)
        self._board = deepcopy(newBrd)
        return newBrd
