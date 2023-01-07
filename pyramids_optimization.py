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


def setNdelValueCol(thisBoard: Board, row, col, value):
    # Set this value for cell at (row, column)
    # and remove it from cell's list in the same column
    thisBoard.board[row][col] = [value]
    for otrCol in range(thisBoard.dim):
        if otrCol != col and value in thisBoard.board[row][otrCol]:
            thisBoard.board[row][otrCol].remove(value)
    return thisBoard


def setNdelValueRow(thisBoard: Board, row, col, value):
    # Set this value for cell at (row, column)
    # and remove it from cell's list in the same row
    thisBoard.board[row][col] = [value]
    for otrRow in range(thisBoard.dim):
        if otrRow != row and value in thisBoard.board[otrRow][col]:
            thisBoard.board[otrRow][col].remove(value)
    return thisBoard


def topCond(topView: list, optBoard: Board):
    # Remember that you should loop col from 0 -> N-1, row = 0
    if not noSolutionCheck(topView):
        raise noSolutionError
    for col, amount in enumerate(topView):
        if amount == 0:
            continue
        elif amount == 1:
            optBoard = setNdelValueCol(optBoard, 0, col, optBoard.dim)
            optBoard = setNdelValueRow(optBoard, 0, col, optBoard.dim)
        elif amount == optBoard.dim:
            for row in range(optBoard.dim):
                optBoard = setNdelValueCol(optBoard, row, col, row+1)
        # else:
        #     pyramidMatrix[0][col] = pyramidMatrix[0][col][:N-amount+1]
        #     for otrRow in range(1, amount):
        #         if N in pyramidMatrix[otrRow][col]:
        #             pyramidMatrix[otrRow][col].remove(N)
    return optBoard


def botCond(botView: list, optBoard: Board):
    # Remember that you should loop col from N-1 -> 0, row = N-1
    if not noSolutionCheck(botView):
        raise noSolutionError
    for col, amount in enumerate(botView):
        if amount == 0:
            continue
        elif amount == 1:
            optBoard = setNdelValueCol(optBoard, optBoard.dim-1, col,
                                       optBoard.dim)
            optBoard = setNdelValueRow(optBoard, optBoard.dim-1, col,
                                       optBoard.dim)
        elif amount == optBoard.dim:
            for row in range(optBoard.dim):
                optBoard = setNdelValueCol(optBoard, row, col,
                                           optBoard.dim-row)
        # else:
        #     pyramidMatrix[N-1][col] = pyramidMatrix[N-1][col][:N-amount+1]
        #     for otrRow in range(N-amount+1, N-1):
        #         if N in pyramidMatrix[otrRow][col]:
        #             pyramidMatrix[otrRow][col].remove(N)
    return optBoard


def rightCond(rightView: list, optBoard: Board):
    # Remember that you should loop row from 0 -> N-1, col = 0
    if not noSolutionCheck(rightView):
        raise noSolutionError
    for row, amount in enumerate(rightView):
        if amount == 0:
            continue
        elif amount == 0:
            continue
        if amount == 1:
            optBoard = setNdelValueRow(optBoard, row, 0, optBoard.dim)
            optBoard = setNdelValueCol(optBoard, row, 0, optBoard.dim)
        elif amount == optBoard.dim:
            for col in range(optBoard.dim):
                setNdelValueRow(optBoard, row, col, col+1)
        # else:
        #     pyramidMatrix[row][0] = pyramidMatrix[row][0][:N-amount+1]
        #     for otrCol in range(1, amount):
        #         if N in pyramidMatrix[row][otrCol]:
        #             pyramidMatrix[row][otrCol].remove(N)
    return optBoard


def leftCond(leftView: list, optBoard: Board):
    # Remember that you should loop row from N-1 -> 0, col = N-1
    if not noSolutionCheck(leftView):
        raise noSolutionError
    for row, amount in enumerate(leftView):
        if amount == 0:
            continue
        elif amount == 1:
            optBoard = setNdelValueRow(optBoard, row, optBoard-1, optBoard)
            optBoard = setNdelValueCol(optBoard, row, optBoard-1, optBoard)
        elif amount == optBoard.dim:
            for col in range(optBoard.dim):
                optBoard = setNdelValueRow(optBoard, row, col,
                                           optBoard.dim-col)
        # else:
        #     pyramidMatrix[row][N-1] = pyramidMatrix[row][N-1][:N-amount+1]
        #     for otrCol in range(N-amount+1, N-1):
        #         if N in pyramidMatrix[row][otrCol]:
        #             pyramidMatrix[row][otrCol].remove(N)
    return optBoard


def remRedundantCond(optBoard: Board):
    for row in range(optBoard.dim):
        for col in range(optBoard.dim):
            if len(optBoard.board[row][col]) == 1:
                optBoard = setNdelValueCol(optBoard, row, col,
                                           optBoard.board[row][col][0])
                optBoard = setNdelValueRow(optBoard, row, col,
                                           optBoard.board[row][col][0])
    return optBoard


def analyzeBasicCond(hints: HintsData):
    condBoard = Board(dim=hints.dim)
    baseList = list(range(1, condBoard.dim+1))
    condBoard.fillBoardWithValue(baseList)

    condBoard = deepcopy(topCond(hints.topView, condBoard))
    condBoard = deepcopy(botCond(hints.botView, condBoard))
    condBoard = deepcopy(rightCond(hints.rightView, condBoard))
    condBoard = deepcopy(leftCond(hints.leftView, condBoard))
    condBoard = deepcopy(remRedundantCond(condBoard))

    return condBoard
