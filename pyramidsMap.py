from copy import deepcopy


class pyrMap():
    def __init__(self, size=0, map=[]):
        self._size = size
        self._map = map

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, lst):
        self._map = lst

    def defaultMapGen(self, defaultValue):
        newMap = []
        for _ in range(self._size):
            rowList = []
            for _ in range(self._size):
                rowList.append(deepcopy(defaultValue))
            newMap.append(rowList)
        self._map = deepcopy(newMap)
        return newMap
