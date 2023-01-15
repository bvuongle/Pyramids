from copy import deepcopy
from exception import NonStandardChars, LengthFileIncorrect


class HintsData():
    def __init__(self, dim=0,
                 topHint=[],
                 botHint=[],
                 rightHint=[],
                 leftHint=[]):
        self._dim = dim
        self._topHint = topHint
        self._botHint = botHint
        self._rightHint = rightHint
        self._leftHint = leftHint

    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, val):
        self._dim = val

    @property
    def topHint(self):
        return self._topHint

    @topHint.setter
    def topHint(self, lst):
        self._topHint = deepcopy(lst)

    @property
    def botHint(self):
        return self._botHint

    @botHint.setter
    def botHint(self, lst):
        self._botHint = deepcopy(lst)

    @property
    def rightHint(self):
        return self._rightHint

    @rightHint.setter
    def rightHint(self, lst):
        self._rightHint = deepcopy(lst)

    @property
    def leftHint(self):
        return self._leftHint

    @leftHint.setter
    def leftHint(self, lst):
        self._leftHint = deepcopy(lst)

    def getData(self, dir):
        f = open(dir, 'r')
        lines = f.read().splitlines()
        # Each input file is only allowed to contain 4 lines,
        # representing the hint for the top, bottom, right and left
        if len(lines) != 4:
            raise LengthFileIncorrect()
        tmpDim = len(lines[0].split(" "))
        if len(lines[1].split(" ")) != tmpDim or \
                len(lines[2].split(" ")) != tmpDim or \
                len(lines[3].split(" ")) != tmpDim:
            raise LengthFileIncorrect()
        try:
            self.dim = tmpDim
            self.topHint = [int(x) for x in lines[0].split(" ")]
            self.botHint = [int(x) for x in lines[1].split(" ")]
            self.rightHint = [int(x) for x in lines[2].split(" ")]
            self.leftHint = [int(x) for x in lines[3].split(" ")]
        except ValueError:
            raise NonStandardChars()
        f.close()
