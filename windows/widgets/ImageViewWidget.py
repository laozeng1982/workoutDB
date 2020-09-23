import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget

from utilities import Utils
from windows.widgets.ImageViewWidgetUI import Ui_Form


class ImageViewWidget(QWidget, Ui_Form):
    """

    """

    def __init__(self, parent=None):
        """
        Path selection widget, a group of widgets to select file or directory.
        :param parent:

        """
        super(ImageViewWidget, self).__init__(parent)
        self.setupUi(self)
        self.label.setStyleSheet('border-width: 1px;border-style: solid; border-color: black')

    def selectImage(self):
        Utils.selectFile(self, "Select Image", self.imagePathEdit.text(), self.imagePathEdit, True,
                         "Images(*.jpg *.png *.gif);;All Files(*.*)")
        self.setPath()

    def setPath(self, path=None):
        if not path:
            path = self.imagePathEdit.text()

        if path.endswith(".png"):
            self.label.setFixedWidth(800)
        else:
            self.label.setFixedSize(300, 300)
        self.imagePathEdit.setText(path)

        if os.path.exists(path):
            if path.endswith(".gif"):
                # print(path)
                gif = QMovie(path)
                gif.setScaledSize(QSize(300, 300))
                self.label.setMovie(gif)
                gif.start()
            else:
                image = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
                self.label.setPixmap(image)
