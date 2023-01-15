from condition_analysis import CondBoard
from board_resolver import BoardResolver
from main_ui import Ui_Piramidy
from error_ui import Ui_Error
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QDialog
import sys
import exception


class ErrorDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Error()
        self.ui.setupUi(self)

    def closeDialog(self):
        self.close()


class PyramidsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Piramidy()
        self.ui.setupUi(self)
        try:
            self.resolver = BoardResolver()
        except exception.WrongDimension:
            self.showError(exception.WrongDimension())
        self.showHome()

    @staticmethod
    def setTableValue(table, data):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                itemValue = str(data[row][col])
                table.setItem(row, col, QTableWidgetItem(itemValue))
                table.item(row, col).setTextAlignment(QtCore.Qt.AlignVCenter
                                                      | QtCore.Qt.AlignHCenter)

    def showHome(self):
        self.ui.mainStack.setCurrentWidget(self.ui.home)
        self.ui.start_btn.clicked.connect(self.showSolve)
        self.ui.help_btn.clicked.connect(self.showHelp)
        self.ui.about_btn.clicked.connect(self.showAbout)
        self.ui.exit_btn.clicked.connect(self.exitProg)

    def showSolve(self):
        self.resetBoard()
        self.ui.mainStack.setCurrentWidget(self.ui.solve)
        self.ui.sizeBoard.valueChanged.connect(self.renewBoard)
        self.ui.reset_btn.clicked.connect(self.resetBoard)
        self.ui.run_btn.clicked.connect(self.getInputData)
        self.ui.openf_btn.clicked.connect(self.getDataFrFile)
        self.ui.save_btn.clicked.connect(self.saveDataToFile)
        self.ui.returnS_btn.clicked.connect(self.showHome)
        self.ui.hintTop.itemChanged.connect(self.clearAnsTable)
        self.ui.hintBot.itemChanged.connect(self.clearAnsTable)
        self.ui.hintRight.itemChanged.connect(self.clearAnsTable)
        self.ui.hintLeft.itemChanged.connect(self.clearAnsTable)

    def showHelp(self):
        self.ui.mainStack.setCurrentWidget(self.ui.help)
        self.ui.returnH_btn.clicked.connect(self.showHome)

    def showAbout(self):
        self.ui.mainStack.setCurrentWidget(self.ui.about)
        self.ui.returnA_btn.clicked.connect(self.showHome)

    def showError(self, error):
        errDlg = ErrorDialog(self)
        errDlg.ui.noti1.setText(str(error))
        errDlg.show()
        errDlg.ui.reset_btn.clicked.connect(self.resetBoard)
        errDlg.ui.reset_btn.clicked.connect(errDlg.closeDialog)
        errDlg.ui.ok_btn.clicked.connect(errDlg.closeDialog)
        return errDlg.exec_()

    def exitProg(self):
        self.close()

    def clearAnsTable(self):
        self.ui.ansTable.clear()

    def renewBoard(self):
        value = self.ui.sizeBoard.value()
        top = self.ui.hintTop
        top.setColumnCount(value)
        top.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setTableValue(top, [[0]*value])

        bot = self.ui.hintBot
        bot.setColumnCount(value)
        bot.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setTableValue(bot, [[0]*value])

        right = self.ui.hintRight
        right.setRowCount(value)
        right.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setTableValue(right, [[0]]*value)

        left = self.ui.hintLeft
        left.setRowCount(value)
        left.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setTableValue(left, [[0]]*value)

        ans = self.ui.ansTable
        ans.setColumnCount(value)
        ans.setRowCount(value)
        ans.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ans.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def resetBoard(self):
        self.ui.save_btn.setEnabled(False)
        self.ui.hintTop.clear()
        self.ui.hintBot.clear()
        self.ui.hintRight.clear()
        self.ui.hintLeft.clear()
        self.ui.ansTable.clear()
        self.renewBoard()

    def getInputData(self) -> bool:
        topHint = botHint = rightHint = leftHint = []
        try:
            for i in range(self.ui.sizeBoard.value()):
                topHint.append(int(self.ui.hintTop.item(0, i).text()))
                botHint.append(int(self.ui.hintBot.item(0, i).text()))
                rightHint.append(int(self.ui.hintRight.item(i, 0).text()))
                leftHint.append(int(self.ui.hintLeft.item(i, 0).text()))
        except ValueError:
            self.showError(exception.NonStandardChars())
            return False

        maxHintsVal = max(max(topHint), max(botHint),
                          max(rightHint), max(leftHint))
        minHintsVal = min(min(topHint), min(botHint),
                          min(rightHint), min(leftHint))
        if maxHintsVal not in range(0, self.ui.sizeBoard.value()+1) or \
                minHintsVal not in range(0, self.ui.sizeBoard.value()+1):
            self.showError(exception.OutsideRange())
            return False

        self.resolver.hints.dim = self.ui.sizeBoard.value()
        self.resolver.renewCurBrd()
        self.resolver.hints.topHint = topHint
        self.resolver.hints.botHint = botHint
        self.resolver.hints.rightHint = rightHint
        self.resolver.hints.leftHint = leftHint
        self.solve()
        return True

    def pasteInputData(self):
        self.ui.sizeBoard.setValue(self.resolver.hints.dim)
        self.renewBoard()
        self.setTableValue(self.ui.hintTop, [self.resolver.hints.topHint])
        self.setTableValue(self.ui.hintBot, [self.resolver.hints.botHint])
        self.setTableValue(self.ui.hintRight,
                           [[x] for x in self.resolver.hints.rightHint])
        self.setTableValue(self.ui.hintLeft,
                           [[x] for x in self.resolver.hints.leftHint])

    def getDataFrFile(self) -> bool:
        self.resetBoard()
        fname = QFileDialog.getOpenFileName(self, "Open File", "./",
                                            "Text Files(*.txt)")

        try:
            self.resolver.hints.getData(fname[0])
        except exception.LengthFileIncorrect:
            self.showError(exception.LengthFileIncorrect())
            return False
        except exception.NonStandardChars:
            self.showError(exception.NonStandardChars())
            return False
        self.pasteInputData()
        return True

    def saveDataToFile(self):
        fname = QFileDialog.getSaveFileName(self, "Save File")
        self.resolver.saveData(fname[0])

    def solve(self) -> None:
        condBase = list(range(1, self.resolver.hints.dim+1))
        self.resolver.condBrd = CondBoard(dim=self.resolver.hints.dim,
                                          base=condBase)
        try:
            self.resolver.condBrd.analyzeBasicCond(self.resolver.hints)
        except exception.NoSolutionError:
            self.showError(exception.NoSolutionError())
            return None

        self.resolver.backtracking(0, 0)

        if self.resolver.flag == 0:
            self.showError(exception.NoSolutionError())
            return None

        self.setTableValue(self.ui.ansTable, self.resolver.curBrd.board)
        self.ui.save_btn.setEnabled(True)
        return None


def guiMain(args):
    app = QApplication(args)
    window = PyramidsWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    guiMain(sys.argv)