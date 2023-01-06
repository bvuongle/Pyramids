class hintsData():
    def __init__(self, N=0, topView=[], botView=[], rightView=[], leftView=[]):
        self._N = N
        self._topView = topView
        self._botView = botView
        self._rightView = rightView
        self._leftView = leftView

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, val):
        self._N = val

    @property
    def topView(self):
        return self._topView

    @topView.setter
    def topView(self, lst):
        self._topView = lst

    @property
    def botView(self):
        return self._botView

    @botView.setter
    def botView(self, lst):
        self._botView = lst

    @property
    def rightView(self):
        return self._rightView

    @rightView.setter
    def rightView(self, lst):
        self._rightView = lst

    @property
    def leftView(self):
        return self._leftView

    @leftView.setter
    def leftView(self, lst):
        self._leftView = lst
