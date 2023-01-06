from copy import deepcopy
from pyramidsMap import pyrMap
from visiblePyramids import hintsData


class noSolutionError(Exception):
    def __init__(self):
        super().__init__("This problem have no solution")


def noSolutionCheck(hint):
    cnt1 = cntN = 0
    for h in hint:
        if h == 1:
            cnt1 += 1
        elif h == len(hint):
            cntN += 1
    return cnt1 <= 1 and cntN <= 1


def delValueColLoop(curMap: pyrMap, row, col, value):
    # Set cell value and delete it from other cell list in the same column
    curMap.map[row][col] = [value]
    for otrCol in range(curMap.size):
        if otrCol != col and value in curMap.map[row][otrCol]:
            curMap.map[row][otrCol].remove(value)
    return curMap


def delValueRowLoop(curMap: pyrMap, row, col, value):
    # Set cell value and delete it from other cell list in the same row
    curMap.map[row][col] = [value]
    for otrRow in range(curMap.size):
        if otrRow != row and value in curMap.map[otrRow][col]:
            curMap.map[otrRow][col].remove(value)
    return curMap


def fromTop(topView: list, orgMap: pyrMap):
    # Remember that you should loop col from 0 -> N-1, row = 0
    if not noSolutionCheck(topView):
        raise noSolutionError
    for col, viewValue in enumerate(topView):
        if viewValue == 0:
            continue
        elif viewValue == 1:
            orgMap = delValueColLoop(orgMap, 0, col, orgMap.size)
            orgMap = delValueRowLoop(orgMap, 0, col, orgMap.size)
        elif viewValue == orgMap.size:
            for row in range(orgMap.size):
                orgMap = delValueColLoop(orgMap, row, col, row+1)
        # else:
        #     pyramidMatrix[0][col] = pyramidMatrix[0][col][:N-viewValue+1]
        #     for otrRow in range(1, viewValue):
        #         if N in pyramidMatrix[otrRow][col]:
        #             pyramidMatrix[otrRow][col].remove(N)
    return orgMap


def fromBot(botView: list, orgMap: pyrMap):
    # Remember that you should loop col from N-1 -> 0, row = N-1
    if not noSolutionCheck(botView):
        raise noSolutionError
    for col, viewValue in enumerate(botView):
        if viewValue == 0:
            continue
        elif viewValue == 1:
            orgMap = delValueColLoop(orgMap, orgMap.size-1, col, orgMap.size)
            orgMap = delValueRowLoop(orgMap, orgMap.size-1, col, orgMap.size)
        elif viewValue == orgMap.size:
            for row in range(orgMap.size):
                orgMap = delValueColLoop(orgMap, row, col, orgMap.size-row)
        # else:
        #     pyramidMatrix[N-1][col] = pyramidMatrix[N-1][col][:N-viewValue+1]
        #     for otrRow in range(N-viewValue+1, N-1):
        #         if N in pyramidMatrix[otrRow][col]:
        #             pyramidMatrix[otrRow][col].remove(N)
    return orgMap


def fromRight(rightView: list, orgMap: pyrMap):
    # Remember that you should loop row from 0 -> N-1, col = 0
    if not noSolutionCheck(rightView):
        raise noSolutionError
    for row, viewValue in enumerate(rightView):
        if viewValue == 0:
            continue
        elif viewValue == 0:
            continue
        if viewValue == 1:
            orgMap = delValueRowLoop(orgMap, row, 0, orgMap.size)
            orgMap = delValueColLoop(orgMap, row, 0, orgMap.size)
        elif viewValue == orgMap.size:
            for col in range(orgMap.size):
                delValueRowLoop(orgMap, row, col, col+1)
        # else:
        #     pyramidMatrix[row][0] = pyramidMatrix[row][0][:N-viewValue+1]
        #     for otrCol in range(1, viewValue):
        #         if N in pyramidMatrix[row][otrCol]:
        #             pyramidMatrix[row][otrCol].remove(N)
    return orgMap


def fromLeft(leftView: list, orgMap: pyrMap):
    # Remember that you should loop row from N-1 -> 0, col = N-1
    if not noSolutionCheck(leftView):
        raise noSolutionError
    for row, viewValue in enumerate(leftView):
        if viewValue == 0:
            continue
        elif viewValue == 1:
            orgMap = delValueRowLoop(orgMap, row, orgMap-1, orgMap)
            orgMap = delValueColLoop(orgMap, row, orgMap-1, orgMap)
        elif viewValue == orgMap.size:
            for col in range(orgMap.size):
                orgMap = delValueRowLoop(orgMap, row, col, orgMap.size-col)
        # else:
        #     pyramidMatrix[row][N-1] = pyramidMatrix[row][N-1][:N-viewValue+1]
        #     for otrCol in range(N-viewValue+1, N-1):
        #         if N in pyramidMatrix[row][otrCol]:
        #             pyramidMatrix[row][otrCol].remove(N)
    return orgMap


def lastReduce(orgMap: pyrMap):
    for row in range(orgMap.size):
        for col in range(orgMap.size):
            if len(orgMap.map[row][col]) == 1:
                orgMap = delValueColLoop(orgMap, row, col,
                                         orgMap.map[row][col][0])  # value
                orgMap = delValueRowLoop(orgMap, row, col,
                                         orgMap.map[row][col][0])  # value
    return orgMap


def reduceConfig(hints: hintsData):
    originalMap = pyrMap(size=hints.N)
    baseList = list(range(1, originalMap.size+1))
    originalMap.defaultMapGen(baseList)
    originalMap = deepcopy(fromTop(hints.topView, originalMap))
    originalMap = deepcopy(fromBot(hints.botView, originalMap))
    originalMap = deepcopy(fromRight(hints.rightView, originalMap))
    originalMap = deepcopy(fromLeft(hints.leftView, originalMap))
    originalMap = deepcopy(lastReduce(originalMap))
    return originalMap
