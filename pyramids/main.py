from hints import HintsData
from board_resolver import BoardResolver
from exception import WrongDimension, LengthFileIncorrect
from exception import NonStandardChars, NoSolutionError, OutsideRange
import argparse
from main_ui import Ui_Piramidy
from error_ui import Ui_Error
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QDialog
import sys
import os


class ErrorDialog(QDialog):
    """Error message interface
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_Error()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./icon/error_icon.png"))

    def closeDialog(self):
        self.close()


class PyramidsWindow(QMainWindow):
    """The main interface of the GUI
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Piramidy()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon("./icon/main_icon.png"))
        try:
            self.prob = BoardResolver()
        except WrongDimension:
            self.showError(WrongDimension())
        self.showHome()

    @staticmethod
    def setTableValue(table, data):
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                itemValue = str(data[row][col])
                table.setItem(row, col, QTableWidgetItem(itemValue))
                table.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)

    def showHome(self):
        """Display home screen interface
        """
        self.ui.mainStack.setCurrentWidget(self.ui.home)
        self.ui.start_btn.clicked.connect(self.showSolve)
        self.ui.help_btn.clicked.connect(self.showHelp)
        self.ui.about_btn.clicked.connect(self.showAbout)
        self.ui.exit_btn.clicked.connect(self.exitProg)

    def showSolve(self):
        """Display solve screen interface
        """
        self.resetBoard()
        self.ui.mainStack.setCurrentWidget(self.ui.solve)
        self.ui.sizeBoard.valueChanged.connect(self.resetBoard)
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
        """Display help screen interface
        """
        self.ui.mainStack.setCurrentWidget(self.ui.help)
        self.ui.returnH_btn.clicked.connect(self.showHome)

    def showAbout(self):
        """Display about screen interface
        """
        self.ui.mainStack.setCurrentWidget(self.ui.about)
        self.ui.returnA_btn.clicked.connect(self.showHome)

    def showError(self, error):
        """Display error screen interface

        :param error: type of error
        :type error: Exception
        """
        errDlg = ErrorDialog(self)
        errDlg.ui.msg.setText(str(error))
        errDlg.show()
        errDlg.ui.reset_btn.clicked.connect(self.resetBoard)
        errDlg.ui.reset_btn.clicked.connect(errDlg.closeDialog)
        errDlg.ui.ok_btn.clicked.connect(errDlg.closeDialog)
        return errDlg.exec_()

    def exitProg(self):
        self.close()

    def clearAnsTable(self):
        self.ui.ansTable.clear()
        self.ui.run_btn.setEnabled(True)

    def renewBoard(self):
        """Change the size of the board display interface
        according to the size selected by the user
        """
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
        """Reset all solve screen interface to default
        """
        self.ui.save_btn.setEnabled(False)
        self.ui.run_btn.setEnabled(True)
        self.ui.hintTop.clear()
        self.ui.hintBot.clear()
        self.ui.hintRight.clear()
        self.ui.hintLeft.clear()
        self.ui.ansTable.clear()
        self.renewBoard()

    def getInputData(self) -> bool:
        """Read input data entered from the user through the GUI
        and run the method to solve it.
        """
        self.ui.run_btn.setEnabled(False)
        topHint, botHint, rightHint, leftHint = ([] for _ in range(4))
        for i in range(self.ui.sizeBoard.value()):
            topHint.append(self.ui.hintTop.item(0, i).text())
            botHint.append(self.ui.hintBot.item(0, i).text())
            rightHint.append(self.ui.hintRight.item(i, 0).text())
            leftHint.append(self.ui.hintLeft.item(i, 0).text())
        try:
            hints = HintsData(self.ui.sizeBoard.value(),
                              topHint, botHint, rightHint, leftHint)
        except NonStandardChars:
            self.showError(NonStandardChars())
            return False
        except OutsideRange:
            self.showError(OutsideRange())
            return False
        except FileNotFoundError:
            return False
        self.solve(hints)
        return True

    def getDataFrFile(self) -> bool:
        """Read input data from file and display it on GUI
        """
        self.resetBoard()
        fname = QFileDialog.getOpenFileName(self, "Open File", "./",
                                            "Text Files(*.txt)")

        try:
            hints = HintsData()
            hints.getData(fname[0])
        except LengthFileIncorrect:
            self.showError(LengthFileIncorrect())
            return False
        except NonStandardChars:
            self.showError(NonStandardChars())
            return False
        except FileNotFoundError:
            return False
        self.pasteInputData(hints)
        return True

    def pasteInputData(self, hints: HintsData):
        """Display input datasets to GUI
        """
        self.ui.sizeBoard.setValue(hints.dim)
        self.renewBoard()
        self.setTableValue(self.ui.hintTop, [hints.topHint])
        self.setTableValue(self.ui.hintBot, [hints.botHint])
        self.setTableValue(self.ui.hintRight,
                           [[x] for x in hints.rightHint])
        self.setTableValue(self.ui.hintLeft,
                           [[x] for x in hints.leftHint])

    def saveDataToFile(self) -> bool:
        """Save the result (if exists) to file
        """
        fname = QFileDialog.getSaveFileName(self, "Save File")
        try:
            self.prob.saveData(fname[0])
            os.startfile(fname[0])
            return True
        except FileNotFoundError:
            return False

    def solve(self, hints: HintsData) -> None:
        """Method solves the problem and prints it to the GUI.
        This method receives input data read from the GUI

        :param hints: Input data read from GUI
        :type hints: HintsData
        """
        self.prob = BoardResolver(hints)
        try:
            self.prob.resolver()
        except NoSolutionError:
            self.showError(NoSolutionError())
            return None

        self.setTableValue(self.ui.ansTable, self.prob.curBrd.board)
        self.ui.save_btn.setEnabled(True)
        return None


def rapidSolver(dir: str) -> BoardResolver:
    """Method used to solve the problem without the need for a GUI.
    Required to get the path to the input data file

    :param dir: path to input data file
    :type dir: str
    :return: object carries the solution of the problem (if exists)
    :rtype: BoardResolver
    """
    hints = HintsData()
    hints.getData(dir)
    prob = BoardResolver(hints)
    prob.resolver()
    return prob


def guiMain(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", nargs="+",  help="Path to input file")
    parser.add_argument("-o", "--output", help="Path to output file")
    arguments = parser.parse_args()
    if arguments.input:
        path = os.path.join(os.path.abspath(os.path.join(
                                                    os.getcwd(),
                                                    os.pardir)
                                            ),
                            arguments.input[0])
        if arguments.output:
            rapidSolver(path).saveData(arguments.output)
    else:
        app = QApplication(args)
        window = PyramidsWindow()
        window.show()
        return app.exec_()


if __name__ == "__main__":
    guiMain(sys.argv)
