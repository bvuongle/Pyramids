from hints_io import read_data_from_file, write_data_to_file
from hints import HintsData
from board import Board
from pyramids_optimization import analyzeBasicCond
from pyramids_backtracking import backtracking


def main():
    hints = HintsData()
    hints = read_data_from_file("./test/pyramid_test_1.txt")
    condBrd = Board()
    condBrd = (analyzeBasicCond(hints))

    curPyrBrd = Board()
    ansMap = Board()
    curPyrBrd.dim = condBrd.dim
    ansMap.dim = condBrd.dim
    curPyrBrd.fillBoardWithValue(0)
    backtracking(curPyrBrd, 0, 0, condBrd, hints, ansMap)
    write_data_to_file("./ans.txt", ansMap.board)


if __name__ == "__main__":
    main()
