from hints_io import read_data_from_file, write_data_to_file
from hints import HintsData
from board import Board
from pyramids_optimization import analyzeBasicCond
from pyramids_backtracking import backtracking
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from main_ui import Ui_MainWindow
import sys


class pyramidsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showHome()

    def showHome(self):
        self.ui.mainStack.setCurrentWidget(self.ui.home)
        self.ui.start_btn.clicked.connect(self.showSolve)
        self.ui.help_btn.clicked.connect(self.showHelp)
        self.ui.about_btn.clicked.connect(self.showAbout)
        self.ui.exit_btn.clicked.connect(self.exitProg)

    def showSolve(self):
        self.renewBoard()
        self.ui.mainStack.setCurrentWidget(self.ui.solve)
        self.ui.sizeBoard.valueChanged.connect(self.renewBoard)
        self.ui.reset_btn.clicked.connect(self.resetBoard)
        self.ui.run_btn.clicked.connect(self.solve)
        self.ui.import_btn.clicked.connect(self.getDataFrFile)

    def showHelp(self):
        self.ui.mainStack.setCurrentWidget(self.ui.help)
        self.ui.return_btn.clicked.connect(self.showHome)

    def showAbout(self):
        self.ui.mainStack.setCurrentWidget(self.ui.about)

    def exitProg(self):
        self.close()

    def setTableValue(self, table, data):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                itemValue = str(data[row][col])
                table.setItem(row, col, QTableWidgetItem(itemValue))
                table.item(row, col).setTextAlignment(QtCore.Qt.AlignVCenter
                                                      | QtCore.Qt.AlignHCenter)

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
        self.ui.hintTop.clear()
        self.ui.hintBot.clear()
        self.ui.hintRight.clear()
        self.ui.hintLeft.clear()
        self.ui.ansTable.clear()
        self.ui.sizeBoard.setValue(1)
        self.renewBoard()

    def getInputData(self):
        self.ui.debug.setText("Data changed")
        topHint = []
        botHint = []
        rightHint = []
        leftHint = []
        for i in range(self.ui.sizeBoard.value()):
            topHint.append(int(self.ui.hintTop.item(0, i).text()))
            botHint.append(int(self.ui.hintBot.item(0, i).text()))
            rightHint.append(int(self.ui.hintRight.item(i, 0).text()))
            leftHint.append(int(self.ui.hintLeft.item(i, 0).text()))
        return HintsData(self.ui.sizeBoard.value(),
                         topHint, botHint, rightHint, leftHint)

    def pasteInputData(self, hints: HintsData):
        self.ui.sizeBoard.setValue(hints.dim)
        self.renewBoard()
        self.setTableValue(self.ui.hintTop, [hints.topHint])
        self.setTableValue(self.ui.hintBot, [hints.botHint])
        self.setTableValue(self.ui.hintRight, [[x] for x in hints.rightHint])
        self.setTableValue(self.ui.hintLeft, [[x] for x in hints.leftHint])
        return None

    def solve(self):
        hints = self.getInputData()
        condBrd = analyzeBasicCond(hints)
        curPyrBrd = Board(dim=condBrd.dim)
        ansMap = Board(dim=condBrd.dim)
        curPyrBrd.fillBoardWithValue(0)
        backtracking(curPyrBrd, 0, 0, condBrd, hints, ansMap)
        # print(ansMap.board[0][0])
        self.setTableValue(self.ui.ansTable, ansMap.board)

    def getDataFrFile(self) -> HintsData:
        fname = QFileDialog.getOpenFileName(self, "Open File", "./",
                                            "Text Files(*.txt)")
        hints = read_data_from_file(fname[0])
        self.pasteInputData(hints)
        return hints


def guiMain(args):
    app = QApplication(args)
    window = pyramidsWindow()
    window.show()
    return app.exec_()


def main():
    hints = HintsData()
    hints = read_data_from_file("./test/pyramid_test_5.txt")
    print([[x] for x in hints.leftHint])
    # condBrd = Board()
    # condBrd = (analyzeBasicCond(hints))
    # print(condBrd.board)
    # curPyrBrd = Board(dim=condBrd.dim)
    # ansMap = Board(dim=condBrd.dim)
    # curPyrBrd.fillBoardWithValue(0)
    # backtracking(curPyrBrd, 0, 0, condBrd, hints, ansMap)
    # write_data_to_file("./ans.txt", ansMap.board)


if __name__ == "__main__":
    guiMain(sys.argv)
    # main()
