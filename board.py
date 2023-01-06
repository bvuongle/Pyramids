from copy import deepcopy


class Board():
    def __init__(self, size=0, map=[]):
        self._size = size
        self._board = map

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, lst):
        self._board = lst

    def defaultMapGen(self, defaultValue):
        newMap = []
        for _ in range(self._size):
            rowList = []
            for _ in range(self._size):
                rowList.append(deepcopy(defaultValue))
            newMap.append(rowList)
        self._board = deepcopy(newMap)
        return newMap
