import sys

from PyQt5.QtWidgets import *

from utilities import Utils
from windows.ActionsCollectorWindow import ActionsCollectorWindow

if __name__ == "__main__":
    """
    主程序入口，所有路径都是从这里起，使用相对路径“.\\”
    """
    app = QApplication(sys.argv)

    window = QMainWindow()
    if Utils.isRunningInChineseDirectory():
        QMessageBox.critical(window, u"错误", u"本程序不能运行在含有中文的目录下，请将程序移至非中文目录。")
        window.close()
        print("Can not run in directory name with Chinese character, program exiting!")
        sys.exit(-1)
    else:
        window.close()

    mainWindow = ActionsCollectorWindow()
    mainWindow.show()

    sys.exit(app.exec_())
