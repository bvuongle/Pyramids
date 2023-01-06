from pyramidsMap import pyrMap
from visiblePyramids import hintsData
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


def checkValidView(curPyrMap: pyrMap, hints: hintsData):
    for it in range(0, hints.N):
        viewTop = hints.topView[it]
        viewBot = hints.botView[it]
        col = it
        tmp = []
        for row in range(0, curPyrMap.size):
            tmp.append(curPyrMap.map[row][col])
        visible_pyr_top = num_visible_pyramids(tmp)
        visible_pyr_bot = num_visible_pyramids(tmp[::-1])
        if (visible_pyr_top != viewTop and viewTop != 0) or \
                (visible_pyr_bot != viewBot and viewBot != 0):
            return False
        else:
            continue
    for it in range(0, hints.N):
        viewRight = hints.rightView[it]
        viewLeft = hints.leftView[it]
        row = it
        tmp = []
        for col in range(0, curPyrMap.size):
            tmp.append(curPyrMap.map[row][col])
        visible_pyr_right = num_visible_pyramids(tmp)
        visible_pyr_left = num_visible_pyramids(tmp[::-1])
        if (visible_pyr_right != viewRight and viewRight != 0) or \
                (visible_pyr_left != viewLeft and viewLeft != 0):
            return False
        else:
            continue
    return True


def backtracking(curPyrMap, row, col, baseMap, hints, ansMap):
    if row == curPyrMap.size-1 and col > curPyrMap.size-1:
        if checkValidView(curPyrMap, hints):
            ansMap.map = deepcopy(curPyrMap.map)
            return ansMap
    else:
        if row < curPyrMap.size-1 and col > curPyrMap.size-1:
            row += 1
            col = 0
        fullSet = set(range(1, curPyrMap.size+1))
        rowSet = set(getRow(curPyrMap.map, row))
        colSet = set(getCol(curPyrMap.map, col))
        remain = fullSet - rowSet - colSet
        for value in remain:
            if value in baseMap.map[row][col]:
                curPyrMap.map[row][col] = value
                backtracking(curPyrMap, row, col+1, baseMap, hints, ansMap)
                curPyrMap.map[row][col] = 0
