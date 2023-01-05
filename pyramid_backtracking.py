def createAnswerPyramidMatrix(N):
    answerPyramidMatrix = []
    for _ in range(N):
        rowList = []
        for _ in range(N):
            rowList.append(0)
        answerPyramidMatrix.append(rowList)
    return answerPyramidMatrix


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


def checkValidView():
    for it in range(0, N):
        viewTop = view[0][it]
        viewBot = view[1][it]
        col = it
        tmp = []
        for row in range(0, N):
            tmp.append(answerPyramidMatrix[row][col])
        visible_pyr_top = num_visible_pyramids(tmp)
        visible_pyr_bot = num_visible_pyramids(tmp[::-1])
        if (visible_pyr_top != viewTop and viewTop != 0) or (visible_pyr_bot != viewBot and viewBot != 0):
            return False
        else: 
            continue
    for it in range(0, N):
        viewRight = view[2][it]
        viewLeft = view[3][it]
        row = it
        tmp = []
        for col in range(0, N):
            tmp.append(answerPyramidMatrix[row][col])
        visible_pyr_right = num_visible_pyramids(tmp)
        visible_pyr_left = num_visible_pyramids(tmp[::-1])
        if (visible_pyr_right != viewRight and viewRight != 0) or (visible_pyr_left != viewLeft and viewLeft != 0):
            return False
        else: 
            continue 
    print(answerPyramidMatrix)
        

def backtracking(row, col):
    if row == N-1 and col > N-1:
        return checkValidView()
    else: 
        if row < N-1 and col > N-1:
            row += 1
            col = 0
        fullSet = set(range(1, N+1))
        rowSet = set(getRow(answerPyramidMatrix, row))
        colSet = set(getCol(answerPyramidMatrix, col))
        remain = fullSet - rowSet - colSet
        #print(remain, row, col)
        for value in remain:
            # @TODO Loại các option đã được chon
            # @TODO Áp dụng thuật loại bỏ, giảm weight
            answerPyramidMatrix[row][col] = value
            backtracking(row, col+1)
            answerPyramidMatrix[row][col] = 0


def main():
    global N, answerPyramidMatrix, view
    N = 5
    view = [
        [0, 0, 3, 0, 1],
        [0, 0, 0, 3, 4],
        [4, 4, 0, 1, 0], 
        [0, 0, 3, 0, 0]
    ]
    answerPyramidMatrix = createAnswerPyramidMatrix(N)
    
    backtracking(0, 0)


if __name__ == "__main__":
    main()