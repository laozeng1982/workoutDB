"""
Base Ascii data table which will be inherited by other data table.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# author: JianGe, created on: 2018/11/11

from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex, Qt

from datamodel.Action import Action
from windows.BaseTableView import BaseTableView
from windows.progress.ProgressWindow import UserThread


class ActionsDataTableView(BaseTableView):
    """
    Customized table view base on BaseTableView (inherit from QTableView), this table will be inherited for other data.
    """

    def __init__(self, parent=None, withCheckBox=None):
        """

        :param parent:
        :param withCheckBox:
        """
        super().__init__(parent, withCheckBox)
        # print("AsciiDataTableView called!")

        self.Parent = parent

        # table settings
        self.customContextMenuRequested.connect(self.showTableBodyPopMenu)
        self.clicked['QModelIndex'].connect(self.clickCell)
        #
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.setSortingEnabled(False)
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)

    def initialize(self, headers: list, rows: list, thread: UserThread = None):
        """

        :param rows:
        :param thread:
        :param headers:
        :return:
        """
        self.makeTableModel(headers, rows, thread=thread)

    def clickCell(self, qModelIndex: QModelIndex):
        """

        :param qModelIndex:
        :return:
        """
        row = qModelIndex.row()

        action = Action()
        for column in range(self.Model.columnCount()):
            name = self.Model.headerData(column, Qt.Horizontal)
            value = self.itemAt(row, column)
            action.set(name, value)

        self.Parent.onActionSelected(action)
