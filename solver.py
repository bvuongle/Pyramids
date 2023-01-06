from hints_io import read_data_from_file, write_data_to_file
from hints import HintsData
from board import Board
from pyramids_optimization import reduceConfig
from pyramids_backtracking import backtracking


def main():
    hints = HintsData()
    hints = read_data_from_file("./test/pyramid_test_2.txt")
    baseMap = Board()
    baseMap = (reduceConfig(hints))

    curPyrBoard = Board()
    ansMap = Board()
    curPyrBoard.size = baseMap.size
    ansMap.size = baseMap.size
    curPyrBoard.defaultMapGen(0)
    backtracking(curPyrBoard, 0, 0, baseMap, hints, ansMap)
    write_data_to_file("./ans.txt", ansMap.board)


if __name__ == "__main__":
    main()
