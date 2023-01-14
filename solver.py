from hints_io import read_data_from_file, write_data_to_file
from hints import HintsData
from board import Board
from copy import deepcopy
from pyramids_optimization import analyzeBasicCond
from pyramids_backtracking import backtracking
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from main_ui import Ui_Piramidy
import sys


class pyramidsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Piramidy()
        self.ui.setupUi(self)
        self.hints = HintsData()
        self.ansBoard = Board()
        self.showHome()

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
        self.ui.run_btn.clicked.connect(self.solve)
        self.ui.openf_btn.clicked.connect(self.getDataFrFile)
        self.ui.save_btn.clicked.connect(self.pasteDataToFile)
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

    def exitProg(self):
        self.close()

    def clearAnsTable(self):
        self.ui.ansTable.clear()

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
        self.ui.save_btn.setEnabled(False)
        self.ui.hintTop.clear()
        self.ui.hintBot.clear()
        self.ui.hintRight.clear()
        self.ui.hintLeft.clear()
        self.ui.ansTable.clear()
        self.ui.sizeBoard.setValue(1)
        self.renewBoard()

    def getInputData(self) -> HintsData:
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

    def getDataFrFile(self) -> HintsData:
        self.resetBoard()
        fname = QFileDialog.getOpenFileName(self, "Open File", "./",
                                            "Text Files(*.txt)")
        hints = read_data_from_file(fname[0])
        self.pasteInputData(hints)
        return hints

    def pasteDataToFile(self):
        fname = QFileDialog.getSaveFileName(self, "Save File")
        write_data_to_file(fname[0], self.hints, self.ansBoard)

    def solve(self):
        self.hints = deepcopy(self.getInputData())
        condBrd = analyzeBasicCond(self.hints)
        curPyrBrd = Board(dim=condBrd.dim)
        self.ansBoard = deepcopy(Board(dim=condBrd.dim))
        curPyrBrd.fillBoardWithValue(0)
        backtracking(curPyrBrd, 0, 0, condBrd, self.hints, self.ansBoard)
        self.setTableValue(self.ui.ansTable, self.ansBoard.board)
        self.ui.save_btn.setEnabled(True)


def guiMain(args):
    app = QApplication(args)
    window = pyramidsWindow()
    window.show()
    return app.exec_()


def main():
    hints = HintsData()
    hints = read_data_from_file("./test/pyramid_test_1.txt")
    condBrd = Board()
    condBrd = (analyzeBasicCond(hints))
    curPyrBrd = Board(dim=condBrd.dim)
    ansMap = Board(dim=condBrd.dim)
    curPyrBrd.fillBoardWithValue(0)
    backtracking(curPyrBrd, 0, 0, condBrd, hints, ansMap)
    write_data_to_file("./ans.txt", hints, ansMap)


if __name__ == "__main__":
    guiMain(sys.argv)
    # main()
