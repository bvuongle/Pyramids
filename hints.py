from copy import deepcopy
from exception import NonStandardChars, LengthFileIncorrect, OutsideRange


class HintsData():
    def __init__(self, dim=0,
                 topHint=[], botHint=[],
                 rightHint=[], leftHint=[]):
        tmpDim = self.checkDim([topHint, botHint, rightHint, leftHint])
        self._dim = tmpDim if tmpDim and dim != tmpDim else dim
        self._topHint = self.checkHint(topHint)
        self._botHint = self.checkHint(botHint)
        self._rightHint = self.checkHint(rightHint)
        self._leftHint = self.checkHint(leftHint)

    @staticmethod
    def checkDim(lists):
        tmpDim = len(lists[0])
        if len(lists[1]) != tmpDim or \
                len(lists[2]) != tmpDim or \
                len(lists[3]) != tmpDim:
            raise LengthFileIncorrect()
        return tmpDim

    def checkHint(self, lst):
        try:
            validHint = [int(x) for x in lst]
        except ValueError:
            raise NonStandardChars()
        if validHint:
            maxVal = max(validHint)
            minVal = min(validHint)
            if maxVal not in range(0, self.dim+1) or \
                    minVal not in range(0, self.dim+1):
                raise OutsideRange()
        return validHint

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
        self._topHint = deepcopy(self.checkHint(lst))

    @property
    def botHint(self):
        return self._botHint

    @botHint.setter
    def botHint(self, lst):
        self._botHint = deepcopy(self.checkHint(lst))

    @property
    def rightHint(self):
        return self._rightHint

    @rightHint.setter
    def rightHint(self, lst):
        self._rightHint = deepcopy(self.checkHint(lst))

    @property
    def leftHint(self):
        return self._leftHint

    @leftHint.setter
    def leftHint(self, lst):
        self._leftHint = deepcopy(self.checkHint(lst))

    def getData(self, dir):
        try:
            f = open(dir, 'r')
        except FileNotFoundError:
            raise FileNotFoundError()
        lines = f.read().splitlines()
        """
        Each input file is only allowed to contain 4 lines,
        representing the hint for the top, bottom, right and left
        """
        if len(lines) != 4:
            raise LengthFileIncorrect()
        self.dim = self.checkDim([line.split(" ") for line in lines])
        self.topHint = lines[0].split(" ")
        self.botHint = lines[1].split(" ")
        self.rightHint = lines[2].split(" ")
        self.leftHint = lines[3].split(" ")

        f.close()
