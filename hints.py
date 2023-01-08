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
        self._topHint = lst

    @property
    def botHint(self):
        return self._botHint

    @botHint.setter
    def botHint(self, lst):
        self._botHint = lst

    @property
    def rightHint(self):
        return self._rightHint

    @rightHint.setter
    def rightHint(self, lst):
        self._rightHint = lst

    @property
    def leftHint(self):
        return self._leftHint

    @leftHint.setter
    def leftHint(self, lst):
        self._leftHint = lst
