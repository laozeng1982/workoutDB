#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   DialogDemo.py    
@Contact :   Do not contact me, thanks.
@License :   (C)Copyright 2017-2018, JianGe

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020/9/21 17:22   JianGe      1.0         None
"""

# import lib
import sys

from PyQt5.QtWidgets import QDialog, QApplication

from windows.DialogDemoUI import Ui_DemoDialog


class DialogDemo(QDialog, Ui_DemoDialog):
    def __init__(self, parent=None):
        super(DialogDemo, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建对话框
    dialog = DialogDemo()
    # 显示对话框
    dialog.show()

    sys.exit(app.exec_())
