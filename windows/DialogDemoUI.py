# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogDemoUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DemoDialog(object):
    def setupUi(self, DemoDialog):
        DemoDialog.setObjectName("DemoDialog")
        DemoDialog.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        DemoDialog.setFont(font)
        self.gridLayout_2 = QtWidgets.QGridLayout(DemoDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(DemoDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(DemoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DemoDialog)
        self.buttonBox.accepted.connect(DemoDialog.accept)
        self.buttonBox.rejected.connect(DemoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DemoDialog)

    def retranslateUi(self, DemoDialog):
        _translate = QtCore.QCoreApplication.translate
        DemoDialog.setWindowTitle(_translate("DemoDialog", "Dialog"))
        self.label.setText(_translate("DemoDialog", "This is a demo.123"))
