# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressWindow(object):
    def setupUi(self, ProgressWindow):
        ProgressWindow.setObjectName("ProgressWindow")
        ProgressWindow.resize(400, 120)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        ProgressWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(ProgressWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout.addWidget(self.timeLabel, 1, 0, 1, 1)
        ProgressWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ProgressWindow)
        self.pushButton.clicked.connect(ProgressWindow.cancel)
        QtCore.QMetaObject.connectSlotsByName(ProgressWindow)

    def retranslateUi(self, ProgressWindow):
        _translate = QtCore.QCoreApplication.translate
        ProgressWindow.setWindowTitle(_translate("ProgressWindow", "Processing"))
        self.pushButton.setText(_translate("ProgressWindow", "Cancel"))
        self.label.setText(_translate("ProgressWindow", "Plese wait..."))
        self.timeLabel.setText(_translate("ProgressWindow", "Spend:"))
