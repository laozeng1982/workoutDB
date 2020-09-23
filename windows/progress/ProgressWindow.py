from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow

from windows.progress.ProgressWindowUI import Ui_ProgressWindow


class ProgressWindow(QMainWindow, Ui_ProgressWindow):
    """
    Progress window, run threads when some operation takes more time.
    """
    percentageTrigger = pyqtSignal(int)
    resultsTrigger = pyqtSignal(object)

    def __init__(self, parent, title="Processing", action=None, *args):
        super(ProgressWindow, self).__init__(parent)
        self.setupUi(self)

        self.Parent = parent
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        # Finished flag
        self.Finished = False
        self.SpendTime = 0

        self.setWindowTitle(title)

        self.userThread = UserThread(self, action, *args)

    def exec(self):
        """

        :return:
        """
        self.show()
        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.setTime)
        self.userThread.percentageTrigger.connect(self.changePercentage)
        self.userThread.resultsTrigger.connect(self.onThreadFinished)
        self.userThread.start()

    def setTime(self):
        """

        :return:
        """
        self.SpendTime += 1
        self.timeLabel.setText("Spend %s seconds" % self.SpendTime)

    def changePercentage(self, percentage):
        """

        :param percentage:
        :return:
        """
        self.progressBar.setValue(int(percentage))
        if int(percentage) >= 100:
            self.Finished = True
            self.close()

    def onThreadFinished(self, result):
        """
        When thread finished normally, send signal and close.
        :param result:
        :return:
        """
        self.resultsTrigger.emit(result)
        self.close()

    def closeEvent(self, event: QCloseEvent):
        """"
        Close event, when thread finished or user cancel, close and exit, otherwise ignore close event.
        """
        if self.Finished:
            event.accept()
            # return 1
        else:
            event.ignore()
            # return 0

    def cancel(self):
        """
        Canceled by user.
        :return:
        """
        print("canceled!")
        self.userThread.terminate()
        self.userThread.wait()
        self.userThread.exit()
        self.Finished = True
        self.close()


class UserThread(QThread):
    """
    User defined thread, running in progress windows.
    """
    percentageTrigger = pyqtSignal(int)
    resultsTrigger = pyqtSignal(object)

    def __init__(self, parent, action, *args):
        super().__init__()
        self.Parent = parent
        self.action = action
        self.args = args

    def run(self) -> None:
        """

        :return:
        """
        if self.action:
            if self.args:
                self.action(thread=self, *self.args)
            else:
                self.action(thread=self)
