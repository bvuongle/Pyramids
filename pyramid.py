class noSolutionError(Exception):
    def __init__(self) -> None:
        super().__init__("This problem have no solution")


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
    # Set cell value and delete it from other cell list in the same column
    pyramidMatrix[row][col] = [value]
    for otrCol in range(N):
        if otrCol != col:
            pyramidMatrix[row][otrCol] = pyramidMatrix[row][otrCol][:value-1] \
                                        + pyramidMatrix[row][otrCol][value:]


def delValueRowLoop(row, col, value):
    # Set cell value and delete it from other cell list in the same row
    pyramidMatrix[row][col] = [value]
    for otrRow in range(N):
        if otrRow != row:
            pyramidMatrix[otrRow][col] = pyramidMatrix[otrRow][col][:value-1] \
                                        + pyramidMatrix[otrRow][col][value:]


def fromTop(topView):
    # Remember that you should loop col from 0 -> N-1
    if not noSolutionCheck(topView):
        raise noSolutionError
    for col, viewValue in enumerate(topView):
        if viewValue == 1:
            delValueColLoop(0, col, N)
            delValueRowLoop(0, col, N)
        elif viewValue == N:
            for row in range(N):
                delValueColLoop(row, col, row+1)


def fromBot(botView):
    # Remember that you should loop row from N-1 -> 0
    if not noSolutionCheck(botView):
        raise noSolutionError
    for col, viewValue in enumerate(botView):
        if viewValue == 1:
            delValueColLoop(N-1, col, N)
            delValueRowLoop(N-1, col, N)
        elif viewValue == N:
            for row in range(N):
                delValueColLoop(row, col, N-row)


def fromRight(rightView):
    # Remember that you should loop row from 0 -> N-1
    if not noSolutionCheck(rightView):
        raise noSolutionError
    for row, viewValue in enumerate(rightView):
        if viewValue == 1:
            delValueRowLoop(row, 0, N)
            delValueColLoop(row, 0, N)
        elif viewValue == N:
            for col in range(N):
                delValueRowLoop(row, col, col+1)


def fromLeft(leftView):
    # Remember that you should loop row from N-1 -> 0
    if not noSolutionCheck(leftView):
        raise noSolutionError
    for row, viewValue in enumerate(leftView):
        if viewValue == 1:
            delValueRowLoop(row, N-1, N)
            delValueColLoop(row, N-1, N)
        elif viewValue == N:
            for col in range(N):
                delValueRowLoop(row, col, N-col)


def reduceConfig(view):
    # Call all above function here
    fromTop(view[0])
    fromBot(view[1])
    fromRight(view[2])
    fromLeft(view[3])


def displayPyramidMatrix():
    for row in pyramidMatrix:
        rowList = []
        for cell in row:
            substr = "".join(str(value) for value in cell)
            rowList.append(substr)
        string = "\t\t".join(rowList)
        print(string, "\n")


def ultimateBacktracking():
    pass


def sudokuBase():
    pass


def main():
    global N, pyramidMatrix
    N = 4
    pyramidMatrix = createPyramidMatrix()
    view = [
            [3, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 4, 0],
            [0, 3, 0, 0]
    ]
    reduceConfig(view)
    displayPyramidMatrix()


if __name__ == "__main__":
    main()
