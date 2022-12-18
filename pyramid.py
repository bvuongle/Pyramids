def noSolutionCheck(view):
    cnt1 = 0
    cntN = 0
    for v in view:
        if v == 1:
            cnt1 += 1
        elif v == N:
            cntN += 1
    return cnt1 <= 1 and cntN <= 1


def createPyramidMatrix():
    baseList = list(range(1, N+1))
    pyramidMatrix = []
    for _ in range(N):
        rowList = []
        for _ in range(N):
            rowList.append(baseList)
        pyramidMatrix.append(rowList)
    return pyramidMatrix


def delValueColLoop(row, col, value):
    pyramidMatrix[row][col] = [value]
    for otrCol in range(N):
        if otrCol != col:
            pyramidMatrix[row][otrCol] = pyramidMatrix[row][otrCol][:value-1] \
                                        + pyramidMatrix[row][otrCol][value:]


def delValueRowLoop(row, col, value):
    pyramidMatrix[row][col] = [value]
    for otrRow in range(N):
        if otrRow != row:
            pyramidMatrix[otrRow][col] = pyramidMatrix[otrRow][col][:value-1] \
                                        + pyramidMatrix[otrRow][col][value:]


def fromTop(topView):
    # Remember that you should loop col from 0 -> N-1
    for col, viewValue in enumerate(topView):
        if viewValue == 1:
            delValueColLoop(0, col, N)
            for row in range(1, N):
                pyramidMatrix[row][col] = pyramidMatrix[row][col][:-1]
        elif viewValue == N:
            for row in range(N):
                delValueColLoop(row, col, row+1)


def fromBot(botView):
    # Remember that you should loop row from N-1 -> 0
    for col, viewValue in enumerate(botView):
        if viewValue == 1:
            delValueColLoop(N-1, col, N)
            pyramidMatrix[N-1][col] = [N]
            for row in range(N-1):
                pyramidMatrix[row][col] = pyramidMatrix[row][col][:-1]
        elif viewValue == N:
            for row in range(N):
                delValueColLoop(row, col, N-row)


def fromRight(rightView):
    # Remember that you should loop row from 0 -> N-1
    for row, viewValue in enumerate(rightView):
        if viewValue == 1:
            delValueRowLoop(row, 0, N)
            for col in range(1, N):
                pyramidMatrix[row][col] = pyramidMatrix[row][col][:-1]
        elif viewValue == N:
            for col in range(N):
                delValueRowLoop(row, col, col+1)


def fromLeft(leftView):
    # Remember that you should loop row from N-1 -> 0
    for row, viewValue in enumerate(leftView):
        if viewValue == 1:
            delValueRowLoop(row, N-1, N)
            for col in range(N-1):
                pyramidMatrix[row][col] = pyramidMatrix[row][col][:-1]
        elif viewValue == N:
            for col in range(N):
                delValueRowLoop(row, col, N-col)


def reduceConfig(pyramidMatrix):
    pass
    # Call all above function here


def sudokuBase():
    pass


def main():
    global N, pyramidMatrix
    N = 4
    pyramidMatrix = createPyramidMatrix()
    fromLeft([4, 0, 0, 0])
    print(pyramidMatrix)


if __name__ == "__main__":
    main()
