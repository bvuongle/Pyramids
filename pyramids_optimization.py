from copy import deepcopy
from board import Board
from hints import HintsData


class noSolutionError(Exception):
    def __init__(self):
        super().__init__("This problem have no solution")


def noSolutionCheck(hint: list):
    cnt_H_min = cnt_H_max = 0
    for amount in hint:
        if amount == 1:
            cnt_H_min += 1
        elif amount == len(hint):
            cnt_H_max += 1
    return cnt_H_min <= 1 and cnt_H_max <= 1


def setNdelValueCol(thisBrd: Board, row, col, value):
    # Set this value for cell at (row, column)
    # and remove it from cell's list in the same column
    thisBrd.board[row][col] = [value]
    for otrCol in range(thisBrd.dim):
        if otrCol != col and value in thisBrd.board[row][otrCol]:
            thisBrd.board[row][otrCol].remove(value)
    return thisBrd


def setNdelValueRow(thisBrd: Board, row, col, value):
    # Set this value for cell at (row, column)
    # and remove it from cell's list in the same row
    thisBrd.board[row][col] = [value]
    for otrRow in range(thisBrd.dim):
        if otrRow != row and value in thisBrd.board[otrRow][col]:
            thisBrd.board[otrRow][col].remove(value)
    return thisBrd


def topCond(topHint: list, optBrd: Board):
    # Remember that you should loop col from 0 -> N-1, row = 0
    if not noSolutionCheck(topHint):
        raise noSolutionError
    for col, amount in enumerate(topHint):
        if amount == 0:
            continue
        elif amount == 1:
            optBrd = setNdelValueCol(optBrd, 0, col, optBrd.dim)
            optBrd = setNdelValueRow(optBrd, 0, col, optBrd.dim)
        elif amount == optBrd.dim:
            for row in range(optBrd.dim):
                optBrd = setNdelValueCol(optBrd, row, col, row+1)
        # else:
        #     pyramidMatrix[0][col] = pyramidMatrix[0][col][:N-amount+1]
        #     for otrRow in range(1, amount):
        #         if N in pyramidMatrix[otrRow][col]:
        #             pyramidMatrix[otrRow][col].remove(N)
    return optBrd


def botCond(botHint: list, optBrd: Board):
    # Remember that you should loop col from N-1 -> 0, row = N-1
    if not noSolutionCheck(botHint):
        raise noSolutionError
    for col, amount in enumerate(botHint):
        if amount == 0:
            continue
        elif amount == 1:
            optBrd = setNdelValueCol(optBrd, optBrd.dim-1, col, optBrd.dim)
            optBrd = setNdelValueRow(optBrd, optBrd.dim-1, col, optBrd.dim)
        elif amount == optBrd.dim:
            for row in range(optBrd.dim):
                optBrd = setNdelValueCol(optBrd, row, col, optBrd.dim-row)
        # else:
        #     pyramidMatrix[N-1][col] = pyramidMatrix[N-1][col][:N-amount+1]
        #     for otrRow in range(N-amount+1, N-1):
        #         if N in pyramidMatrix[otrRow][col]:
        #             pyramidMatrix[otrRow][col].remove(N)
    return optBrd


def rightCond(rightHint: list, optBrd: Board):
    # Remember that you should loop row from 0 -> N-1, col = 0
    if not noSolutionCheck(rightHint):
        raise noSolutionError
    for row, amount in enumerate(rightHint):
        if amount == 0:
            continue
        elif amount == 0:
            continue
        if amount == 1:
            optBrd = setNdelValueRow(optBrd, row, 0, optBrd.dim)
            optBrd = setNdelValueCol(optBrd, row, 0, optBrd.dim)
        elif amount == optBrd.dim:
            for col in range(optBrd.dim):
                setNdelValueRow(optBrd, row, col, col+1)
        # else:
        #     pyramidMatrix[row][0] = pyramidMatrix[row][0][:N-amount+1]
        #     for otrCol in range(1, amount):
        #         if N in pyramidMatrix[row][otrCol]:
        #             pyramidMatrix[row][otrCol].remove(N)
    return optBrd


def leftCond(leftHint: list, optBrd: Board):
    # Remember that you should loop row from N-1 -> 0, col = N-1
    if not noSolutionCheck(leftHint):
        raise noSolutionError
    for row, amount in enumerate(leftHint):
        if amount == 0:
            continue
        elif amount == 1:
            optBrd = setNdelValueRow(optBrd, row, optBrd.dim-1, optBrd)
            optBrd = setNdelValueCol(optBrd, row, optBrd.dim-1, optBrd)
        elif amount == optBrd.dim:
            for col in range(optBrd.dim):
                optBrd = setNdelValueRow(optBrd, row, col, optBrd.dim-col)
        # else:
        #     pyramidMatrix[row][N-1] = pyramidMatrix[row][N-1][:N-amount+1]
        #     for otrCol in range(N-amount+1, N-1):
        #         if N in pyramidMatrix[row][otrCol]:
        #             pyramidMatrix[row][otrCol].remove(N)
    return optBrd


def remRedundantCond(optBrd: Board):
    for row in range(optBrd.dim):
        for col in range(optBrd.dim):
            if len(optBrd.board[row][col]) == 1:
                optBrd = setNdelValueCol(optBrd, row, col,
                                         optBrd.board[row][col][0])
                optBrd = setNdelValueRow(optBrd, row, col,
                                         optBrd.board[row][col][0])
    return optBrd


def analyzeBasicCond(hints: HintsData):
    condBrd = Board(dim=hints.dim)
    baseList = list(range(1, condBrd.dim+1))
    condBrd.fillBoardWithValue(baseList)

    condBrd = deepcopy(topCond(hints.topHint, condBrd))
    condBrd = deepcopy(botCond(hints.botHint, condBrd))
    condBrd = deepcopy(rightCond(hints.rightHint, condBrd))
    condBrd = deepcopy(leftCond(hints.leftHint, condBrd))
    condBrd = deepcopy(remRedundantCond(condBrd))

    return condBrd
