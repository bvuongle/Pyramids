from viewData_io import read_data_from_file, write_data_to_file
from visiblePyramids import hintsData
from pyramidsMap import pyrMap
from pyramid import reduceConfig
from pyramid_backtracking import backtracking


def main():
    hints = hintsData()
    hints = read_data_from_file("./test/pyramid_test_2.txt")
    baseMap = pyrMap()
    baseMap = (reduceConfig(hints))

    curPyrMap = pyrMap()
    ansMap = pyrMap()
    curPyrMap.size = baseMap.size
    ansMap.size = baseMap.size
    curPyrMap.defaultMapGen(0)
    backtracking(curPyrMap, 0, 0, baseMap, hints, ansMap)
    write_data_to_file("./ans.txt", ansMap.map)


if __name__ == "__main__":
    main()
