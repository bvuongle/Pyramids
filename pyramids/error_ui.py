# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/error_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Error(object):
    def setupUi(self, Error):
        Error.setObjectName("Error")
        Error.resize(500, 200)
        self.stackedWidget = QtWidgets.QStackedWidget(Error)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 500, 200))
        self.stackedWidget.setObjectName("stackedWidget")
        self.errormsg = QtWidgets.QWidget()
        self.errormsg.setObjectName("errormsg")
        self.msg = QtWidgets.QLabel(self.errormsg)
        self.msg.setGeometry(QtCore.QRect(20, 20, 451, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.msg.setFont(font)
        self.msg.setText("")
        self.msg.setScaledContents(True)
        self.msg.setAlignment(QtCore.Qt.AlignCenter)
        self.msg.setObjectName("msg")
        self.ok_btn = QtWidgets.QPushButton(self.errormsg)
        self.ok_btn.setGeometry(QtCore.QRect(330, 160, 70, 30))
        self.ok_btn.setObjectName("ok_btn")
        self.reset_btn = QtWidgets.QPushButton(self.errormsg)
        self.reset_btn.setGeometry(QtCore.QRect(420, 160, 70, 30))
        self.reset_btn.setObjectName("reset_btn")
        self.stackedWidget.addWidget(self.errormsg)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Error)
        QtCore.QMetaObject.connectSlotsByName(Error)

    def retranslateUi(self, Error):
        _translate = QtCore.QCoreApplication.translate
        Error.setWindowTitle(_translate("Error", "Warning"))
        self.ok_btn.setText(_translate("Error", "OK"))
        self.reset_btn.setText(_translate("Error", "Reset"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Error = QtWidgets.QDialog()
    ui = Ui_Error()
    ui.setupUi(Error)
    Error.show()
    sys.exit(app.exec_())
