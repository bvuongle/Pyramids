from exception import WrongDimension
from copy import deepcopy


class Board():
    """
    Board class is used to store the data of
    a square board with a specified dimension.
    """
    def __init__(self, dim=0, board=[]):
        """Initializes the Board object.
        If dim is not passed to the function,
        object will take the dimension of the board as its dimension.

        :param dim: dimension of the board, defaults to 0
        :type dim: int, optional
        :param board: data contained in board, defaults to []
        :type board: list, optional
        """
        self.checkDimNBoardRelation(dim, board)
        self._dim = dim if dim != 0 else len(board)
        self._board = board

    def checkDimNBoardRelation(self, dim: int, board: list):
        """Check if in initial tuple the value of dimension
        is equal to the actual dimension in the table.

        :param dim: dimension is passed to the function
        :type dim: int
        :param board: board is passed to the function
        :type board: list
        :raises WrongDimension: exception
        """
        if dim != 0 and board:
            if len(board) != dim:
                raise WrongDimension()

    @property
    def dim(self) -> int:
        """Dimension of the board.

        :return: dimension of this object
        :rtype: int
        """
        return self._dim

    @dim.setter
    def dim(self, val):
        self._dim = val

    @property
    def board(self) -> list:
        """The data contained in the board.

        :return: data of this object
        :rtype: list
        """
        return self._board

    @board.setter
    def board(self, lst):
        self._board = deepcopy(lst)

    def fillBoardWithValue(self, value):
        """Used to fill every cells in the "board" property
        with the value "value". This method will update the
        data of the "board" property and return None

        :param value: Values to be placed in board cells
        :type value: int
        """
        newBrd = []
        for _ in range(self._dim):
            rowList = []
            for _ in range(self._dim):
                rowList.append(deepcopy(value))
            newBrd.append(rowList)
        self._board = deepcopy(newBrd)
