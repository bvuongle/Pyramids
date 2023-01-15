from hints import HintsData
from board import Board
from pyramids_optimization import CondBoard
from board_resolver import BoardResolver
from main_ui import Ui_Piramidy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
import sys


class invalidInputFile(Exception):
    def __init__(self):
        super().__init__("Input data in this file is in the wrong format")


class invalidDataLength(Exception):
    def __init__(self):
        super().__init__("The length of input data is incorrect")


class pyramidsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Piramidy()
        self.ui.setupUi(self)
        self.hints = HintsData()
        self.ansBoard = Board()
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
        self.ui.run_btn.clicked.connect(self.solve)
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
        self.ui.sizeBoard.setValue(1)
        self.renewBoard()

    def getInputData(self) -> None:
        topHint = []
        botHint = []
        rightHint = []
        leftHint = []
        for i in range(self.ui.sizeBoard.value()):
            topHint.append(int(self.ui.hintTop.item(0, i).text()))
            botHint.append(int(self.ui.hintBot.item(0, i).text()))
            rightHint.append(int(self.ui.hintRight.item(i, 0).text()))
            leftHint.append(int(self.ui.hintLeft.item(i, 0).text()))
        self.hints.dim = self.ui.sizeBoard.value()
        self.hints.topHint = topHint
        self.hints.botHint = botHint
        self.hints.rightHint = rightHint
        self.hints.leftHint = leftHint
        return None

    def pasteInputData(self) -> None:
        self.ui.sizeBoard.setValue(self.hints.dim)
        self.renewBoard()
        self.setTableValue(self.ui.hintTop, [self.hints.topHint])
        self.setTableValue(self.ui.hintBot, [self.hints.botHint])
        self.setTableValue(self.ui.hintRight,
                           [[x] for x in self.hints.rightHint])
        self.setTableValue(self.ui.hintLeft,
                           [[x] for x in self.hints.leftHint])
        return None

    def getDataFrFile(self) -> None:
        self.resetBoard()
        fname = QFileDialog.getOpenFileName(self, "Open File", "./",
                                            "Text Files(*.txt)")
        f = open(fname[0], 'r')
        lines = f.read().splitlines()
        # Each input file is only allowed to contain 4 lines,
        # representing the hint for the top, bottom, right and left
        if len(lines) != 4:
            raise invalidDataLength()
        tmpDim = len(lines[0].split(" "))
        if len(lines[1].split(" ")) != tmpDim or \
                len(lines[2].split(" ")) != tmpDim or \
                len(lines[3].split(" ")) != tmpDim:
            raise invalidDataLength()
        try:
            self.hints.dim = tmpDim
            self.hints.topHint = [int(x) for x in lines[0].split(" ")]
            self.hints.botHint = [int(x) for x in lines[1].split(" ")]
            self.hints.rightHint = [int(x) for x in lines[2].split(" ")]
            self.hints.leftHint = [int(x) for x in lines[3].split(" ")]
        except ValueError:
            raise invalidInputFile()
        f.close()
        print(self.hints.topHint)
        self.pasteInputData()
        return None

    def saveDataToFile(self) -> None:
        fname = QFileDialog.getSaveFileName(self, "Save File")
        f = open(fname[0], 'w')
        f.write("Answer to the problem with board size of ")
        f.write(f"N = {self.hints.dim}, and hints is as follows: ")
        f.write("\n[\n")
        f.writelines(f"{x} " for x in self.hints.topHint)
        f.write("\n")
        f.writelines(f"{x} " for x in self.hints.botHint)
        f.write("\n")
        f.writelines(f"{x} " for x in self.hints.rightHint)
        f.write("\n")
        f.writelines(f"{x} " for x in self.hints.leftHint)
        f.write("\n]\n\n")
        f.write("#"*20)
        f.write("\n")
        for row in self.ansBoard.board:
            for cell in row:
                f.write(f"{cell} ")
            f.write("\n")
        f.write("#"*20)
        f.close()
        return None

    def solve(self) -> None:
        self.getInputData()
        condBrd = CondBoard(dim=self.hints.dim,
                            base=list(range(1, self.hints.dim+1)))
        condBrd.analyzeBasicCond(self.hints)
        curPyrBrd = Board(dim=condBrd.dim)
        curPyrBrd.fillBoardWithValue(0)
        resolver = BoardResolver(curPyrBrd, self.hints, condBrd)
        resolver.backtracking(0, 0)
        self.setTableValue(self.ui.ansTable, resolver.curBrd.board)
        self.ansBoard.dim = resolver.curBrd.dim
        self.ansBoard.board = resolver.curBrd.board
        self.ui.save_btn.setEnabled(True)
        return None


def guiMain(args):
    app = QApplication(args)
    window = pyramidsWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    guiMain(sys.argv)
