from copy import deepcopy
from exception import NonStandardChars, LengthFileIncorrect, OutsideRange


class HintsData():
    """HintsData class contains input data, which are indicators of
    how many pyramids can be seen from a given position.\n
    There are four types of hints: topHint, botHint, rightHint, leftHint.\n
    Along with that is the dim parameter that will determine the size of
    the problem.
    """
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
    def checkDim(lists: list) -> int:
        """Check if the list of hint types has the same data length.

        :param lists: list of hint types
        :type lists: list
        :raises LengthFileIncorrect: exception - inconsitent data length
        :return: valid dimension value
        :rtype: int
        """
        tmpDim = len(lists[0])
        if len(lists[1]) != tmpDim or \
                len(lists[2]) != tmpDim or \
                len(lists[3]) != tmpDim:
            raise LengthFileIncorrect()
        return tmpDim

    def checkHint(self, lst: list) -> list:
        """Check if the value in the list of hints is valid.

        :param lst: list of hints
        :type lst: list
        :raises NonStandardChars: exception - data contains non-standard \
        characters - not digits
        :raises OutsideRange: exception - data are numbers outside \
        the range 1 to N, resulting in an unsolved problem
        :return: list of hints data has been normalized
        :rtype: list
        """
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
    def dim(self) -> int:
        """Dimension of the problem

        :return: dimension
        :rtype: int
        """
        return self._dim

    @dim.setter
    def dim(self, val):
        self._dim = val

    @property
    def topHint(self) -> list:
        """Hint at the top of the board applies to the columns viewed \
            from the top.

        :return: Hints of type 1
        :rtype: list
        """
        return self._topHint

    @topHint.setter
    def topHint(self, lst):
        self._topHint = deepcopy(self.checkHint(lst))

    @property
    def botHint(self) -> list:
        """Hint at the bottom of the board applies to the columns viewed \
            from the bottom.

        :return: Hints of type 2
        :rtype: list
        """
        return self._botHint

    @botHint.setter
    def botHint(self, lst):
        self._botHint = deepcopy(self.checkHint(lst))

    @property
    def rightHint(self) -> list:
        """Hint on the right side of the board applies to rows viewed \
            from the right.

        :return: Hints of type 3
        :rtype: list
        """
        return self._rightHint

    @rightHint.setter
    def rightHint(self, lst):
        self._rightHint = deepcopy(self.checkHint(lst))

    @property
    def leftHint(self) -> list:
        """Hint on the left side of the board applies to rows viewed\
            from the left.

        :return: Hints of type 4
        :rtype: list
        """
        return self._leftHint

    @leftHint.setter
    def leftHint(self, lst):
        self._leftHint = deepcopy(self.checkHint(lst))

    def getData(self, dir):
        """Get data from file
        File is only allowed to contain 4 lines,
        representing the hint for the top, bottom, right and left

        :param dir: path to input file
        :type dir: str
        :raises FileNotFoundError: exception - File not found in "dir" path
        :raises LengthFileIncorrect: exception - File contains more or less \
            than 4 lines of data
        """
        try:
            f = open(dir, 'r')
        except FileNotFoundError:
            raise FileNotFoundError()
        lines = f.read().splitlines()
        if len(lines) != 4:
            raise LengthFileIncorrect()
        self.dim = self.checkDim([line.split(" ") for line in lines])
        self.topHint = lines[0].split(" ")
        self.botHint = lines[1].split(" ")
        self.rightHint = lines[2].split(" ")
        self.leftHint = lines[3].split(" ")

        f.close()
