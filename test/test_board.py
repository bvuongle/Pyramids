import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from board import Board  # noqa: E402
from exception import WrongDimension  # noqa: E402
from pytest import raises  # noqa: E402


def test_init_board():
    newBrd = Board(2, [[1, 2], [1, 2]])
    assert newBrd.dim == 2
    assert newBrd.board == [[1, 2], [1, 2]]


def test_init_empty_board():
    emptyBrd = Board()
    assert emptyBrd.dim == 0
    assert emptyBrd.board == []


def test_init_no_dim_provied():
    noDimBrd = Board(board=[[1, 2], [1, 2]])
    assert noDimBrd.dim == 2


def test_init_no_board_provided():
    noBoardBrd = Board(dim=2)
    assert noBoardBrd.dim == 2
    assert noBoardBrd.board == []


def test_init_dimP_diff_dimB():
    with raises(WrongDimension):
        assert Board(4, [[1, 2], [1, 2]]) == str(WrongDimension())


def test_dim_setter():
    newBrd = Board(board=[[1, 2], [1, 2]])
    newBrd.dim = 2
    assert newBrd.dim == 2


def test_board_setter():
    newBrd = Board(dim=3)
    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    newBrd.board = matrix
    assert newBrd.board == matrix and id(newBrd) != id(matrix)


def test_fill_board_with_value():
    newBrd = Board(dim=5)
    newBrd.fillBoardWithValue(3)
    assert newBrd.board == [[3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3],
                            [3, 3, 3, 3, 3]]
