from board import Board
from hints import HintsData
from copy import deepcopy


def getRow(matrix, row):
    return [x for x in matrix[row] if x != 0]


def getCol(matrix, col):
    return [row[col] for row in matrix if row[col] != 0]


def num_visible_pyramids(arr):
    cur = arr[0]
    n = len(arr)
    cnt = 1
    for i in range(1, n):
        if arr[i] > cur:
            cnt += 1
            cur = arr[i]
    return cnt


def checkResultWithCond(curPyrBrd: Board, hints: HintsData):
    for it in range(0, hints.dim):
        topCond = hints.topHint[it]
        botCond = hints.botHint[it]
        rightCond = hints.rightHint[it]
        leftCond = hints.leftHint[it]

        col = it
        tmp = []
        for row in range(0, curPyrBrd.dim):
            tmp.append(curPyrBrd.board[row][col])
        visible_pyr_top = num_visible_pyramids(tmp)
        visible_pyr_bot = num_visible_pyramids(tmp[::-1])

        row = it
        tmp = []
        for col in range(0, curPyrBrd.dim):
            tmp.append(curPyrBrd.board[row][col])
        visible_pyr_right = num_visible_pyramids(tmp)
        visible_pyr_left = num_visible_pyramids(tmp[::-1])

        if (visible_pyr_top != topCond and topCond != 0) or \
                (visible_pyr_bot != botCond and botCond != 0) or \
                (visible_pyr_right != rightCond and rightCond != 0) or \
                (visible_pyr_left != leftCond and leftCond != 0):
            return False
        else:
            continue
    return True


def backtracking(curPyrBrd, row, col, condBrd, hints, ansMap):
    if row == curPyrBrd.dim-1 and col > curPyrBrd.dim-1:
        if checkResultWithCond(curPyrBrd, hints):
            ansMap.board = deepcopy(curPyrBrd.board)
            return ansMap
    else:
        if row < curPyrBrd.dim-1 and col > curPyrBrd.dim-1:
            row += 1
            col = 0
        fullSet = set(range(1, curPyrBrd.dim+1))
        rowSet = set(getRow(curPyrBrd.board, row))
        colSet = set(getCol(curPyrBrd.board, col))
        remain = fullSet - rowSet - colSet
        for value in remain:
            if value in condBrd.board[row][col]:
                curPyrBrd.board[row][col] = value
                backtracking(curPyrBrd, row, col+1, condBrd, hints, ansMap)
                curPyrBrd.board[row][col] = 0
