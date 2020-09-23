"""
Base TableView inherit from QTableView.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# author: JianGe, created on: 2018/10/14

import math
import re

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from utilities import Utils, Chinese
from utilities.LogHelper import logger
from windows.progress.ProgressWindow import UserThread


class BaseTableView(QTableView):
    """
    Base customized table view base on QTableView, add some check status functions and filter.
    Defined 'checked' or 'check' related checkbox operation, 'selected' or 'select' related user selection.
    """

    def __init__(self, parent=None, withCheckBox=True, alignHCenter=True):
        """

        :param parent:
        :param withCheckBox:
        """
        super().__init__(parent)

        self.Parent = parent
        self.ComboBoxStringList = []
        self.rowComboBoxList = []
        self.columnComBoxList = []

        self.withCheckBox = withCheckBox
        self.Model = QStandardItemModel()

        self.alignHCenter = alignHCenter

        # mouse right button click menu
        self.tableBodyPopMenu = QMenu(self)
        self.tableHeaderPopMenu = QMenu(self)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setSortingEnabled(True)

        # self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.horizontalHeader().setStretchLastSection(True)
        # self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        # self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def initialize(self, **kwargs):
        """
        Initialize tableview.
        :param kwargs:
        :return:
        """
        pass

    def makeTableModel(self, headers, rows, thread: UserThread = None, hideIdColumn=False):
        """
        Make source for table.

        :param headers:
        :param rows: table source source
        :param thread:
        :param hideIdColumn: index of columns need to be hide.
        :return:
        """
        self.Model = QStandardItemModel()

        if rows:
            columnCount = len(headers)
        else:
            self.setModel(self.Model)
            return

        # must set column count first, otherwise it won't show correctly.
        self.Model.setColumnCount(columnCount)

        # set default header
        for columnIdx, name in enumerate(headers):
            self.Model.setHeaderData(columnIdx, QtCore.Qt.Horizontal, name)

        # add column data as table source
        length = len(rows)
        for rowIdx, row in enumerate(rows):
            rowModels = []
            if self.withCheckBox:
                chkBoxItem = QtGui.QStandardItem()
                chkBoxItem.setCheckable(True)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                chkBoxItem.setText(str(row[0]))
                rowModels.append(chkBoxItem)
                restRow = row[1:]
            else:
                restRow = row

            for columnIdx, field in enumerate(restRow):
                if columnIdx <= 1:
                    data = field
                elif type(field) == str and field.isdigit():
                    data = field
                else:
                    if isinstance(field, float):
                        if math.isnan(field):
                            data = '0.00'
                        else:
                            data = "%.4f" % field
                    else:
                        data = str(field)

                stdItem = TableCellItem(data)
                if self.alignHCenter:
                    stdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                else:
                    stdItem.setTextAlignment(Qt.AlignVCenter)

                if columnIdx == 0:
                    stdItem.setEditable(False)

                stdItem.setData(data, QtCore.Qt.UserRole)
                rowModels.append(stdItem)

            if thread:
                thread.percentageTrigger.emit(rowIdx * 100 / length)

            self.Model.appendRow(rowModels)

        self.setModel(self.Model)

        if thread:
            thread.percentageTrigger.emit(100)
            thread.resultsTrigger.emit(100)

        if hideIdColumn:
            self.hideColumn(1)
            self.hideColumn(columnCount)

    def afterDataLoaded(self):
        """

        :return:
        """
        pass

    def setButton(self, buttonText):
        """

        :param buttonText:
        :return:
        """
        model = self.model()
        for row in range(model.rowCount()):
            # print("add button", model.rowCount() - 1, model.columnCount())
            button = QPushButton(buttonText)
            button.setProperty("row", row)
            # button.setFixedSize(100, 40)
            button.clicked.connect(self.buttonClick)
            # print("status:", model.index(row, model.columnCount() - 1).data())
            button.setEnabled(model.index(row, model.columnCount() - 1).data() == "True")
            self.setIndexWidget(model.index(row, model.columnCount() - 1), button)

    def setColumnComboBox(self):
        """

        :return:
        """
        self.columnComBoxList = []
        for column in range(self.model().columnCount()):
            index = self.model().index(0, column)
            comboBox = QtWidgets.QComboBox()
            comboBox.addItems(self.ComboBoxStringList)
            comboBox.setCurrentText(index.data())
            comboBox.currentTextChanged["QString"].connect(self.changeColumnComboBox)
            self.setIndexWidget(index, comboBox)
            self.columnComBoxList.append(comboBox)

    def changeColumnComboBox(self, text):
        """

        :param text:
        :return:
        """
        pass

    def setRowComboBox(self):
        """

        :return:
        """
        self.rowComboBoxList = []
        for row in range(self.model().rowCount()):
            comboBox = QtWidgets.QComboBox()
            comboBox.addItems(self.ComboBoxStringList)
            comboBox.currentTextChanged['QString'].connect(self.changeRowComboBox)
            comboBox.setCurrentText(self.model().index(row, 0).data())
            self.setIndexWidget(self.model().index(row, 0), comboBox)
            self.rowComboBoxList.append(comboBox)

    def changeRowComboBox(self, text):
        """

        :param text:
        :return:
        """
        pass

    def showTableBodyPopMenu(self):
        """
        Show table pop header when user right click on table body.
        :return:
        """
        self.tableBodyPopMenu.exec_(QCursor.pos())

    def showTableHeaderPopMenu(self):
        """
        Show table pop header when user right click on table header.
        :return:
        """
        self.tableHeaderPopMenu.exec_(QCursor.pos())

    def rowCount(self):
        """

        :return:
        """
        return self.Model.rowCount()

    def columnCount(self):
        """

        :return:
        """
        return self.Model.columnCount()

    def clickRow(self, qModelIndex):
        """

        :param qModelIndex:
        :return:
        """
        pass

    def keysOfClickedRow(self, qModelIndex, columns: list):
        """
        Get key words in columns when a row clicked.
        :param columns:
        :param qModelIndex:
        :return:
        """
        selectedRow = qModelIndex.row()
        keyWords = []
        # get selected keyword by selected row
        for col in columns:
            # if self.item_at(selectedRow, col):
            keyWords.append(self.itemAt(selectedRow, col))

        return keyWords

    def buttonClick(self):
        """

        :return:
        """
        pass

    def printAllData(self):
        """

        :return:
        """
        for row in range(self.Model.rowCount()):
            rowData = []
            for column in range(self.Model.columnCount()):
                if column == 0:
                    rowData.append(self.indexWidget(self.model().index(row, 0)).currentText())
                else:
                    rowData.append(self.Model.index(row, column).data())
            print("row %s %s" % (row + 1, rowData))

    def checkAllRows(self):
        """
        Check all rows in this table.
        :return:
        """
        self._set_all_rows_check_state(Qt.Checked)

    def checkRowByRowIndex(self, rowIndex):
        """
        Check row by rowIndex.
        :param rowIndex:
        :return:
        """
        self._set_selected_state_by_row(rowIndex, Qt.Checked)

    def checkHighLightRowsByKey(self, key):
        """
        Check highlight rows.
        :param key:
        :return:
        """
        self._set_selected_state_by_key(1, key, Qt.Checked)

    def uncheckAllRows(self):
        """
        Uncheck all rows.
        :return:
        """
        self._set_all_rows_check_state(Qt.Unchecked)

    def uncheckHighLightRowsByKey(self, key):
        """
        Uncheck highlight rows.
        :param key:
        :return:
        """
        self._set_selected_state_by_key(1, key, Qt.Unchecked)

    def checkRowAt(self, rowIdx):
        """
        Set row checked at rowIdx.
        :param rowIdx:
        :return:
        """
        self.Model.item(rowIdx).setCheckState(Qt.Checked)

    def checkHighLightRows(self):
        """
        Check rows which were selected by user.
        :return:
        """
        selectedItemList = list(self.selectedIndexes())
        self._set_selected_rows_check_state(selectedItemList, Qt.Checked)

    def uncheckHighLightRows(self):
        """
        Uncheck rows which were selected by user.
        :return:
        """
        selectedItemList = list(self.selectedIndexes())
        self._set_selected_rows_check_state(selectedItemList, Qt.Unchecked)

    def hasRowChecked(self):
        """

        :return:
        """
        return self._has_row_checked()

    def keysOfCheckedRows(self, key_columns: list):
        """
        Get keys which indicated by 'key_columns' in this table.
        :param key_columns:
        :return:
        """
        rowList = self._all_rows()

        selectedRowList = []
        for row, item in enumerate(rowList):
            if item.checkState() == Qt.Checked and item.isEnabled():
                rowKeys = []
                item.setCheckState(Qt.Unchecked)
                for column in key_columns:
                    rowKeys.append(self.itemAt(row, column))
                selectedRowList.append(rowKeys)

        return selectedRowList

    def keyOfCheckedRows(self, queryColumns):
        """
        Get key words of cell whose row was checked and in the query column.
        :param queryColumns:
        :return:
        """
        rowList = self._all_rows()

        selectedRowKeys = []
        for row, item in enumerate(rowList):
            for query_column in queryColumns:
                if item.checkState() == Qt.Checked and item.isEnabled():
                    rowKey = self.itemAt(row, query_column)
                    selectedRowKeys.append(rowKey)

        return selectedRowKeys

    def indexesOfCheckedRows(self):
        """
        Get indexes of cell whose row was checked.
        :return:
        """
        rowList = self._all_rows()

        selectedRowIndexList = []
        for row, item in enumerate(rowList):
            if item.checkState() == Qt.Checked and item.isEnabled():
                selectedRowIndexList.append(row)

        logger.info(len(selectedRowIndexList))
        logger.info(selectedRowIndexList)
        return selectedRowIndexList

    def keysOfHighLightRows(self, query_columns: list):
        """
        Get key words of cell whose row was checked and in the query columns.
        :param query_columns:
        :return:
        """
        selectedItemList = list(self.selectedIndexes())
        rowIndexSet = set()
        for selectedCell in selectedItemList:
            rowIndexSet.add(selectedCell.row())

        allRows = self._all_rows()

        keyWords = []

        for row, item in enumerate(allRows):
            if row in rowIndexSet:
                keyWord = []
                for column in query_columns:
                    keyWord.append(self.itemAt(row, column))
                keyWords.append(keyWord)

        return keyWords

    def itemAt(self, row: int, column: int):
        """
        Get item value at (row, column).
        :param row:
        :param column:
        :return:
        """
        if row == -1:
            row = self.model().rowCount() - 1
        return self.Model.index(row, column).data()

    def removeAllRows(self):
        """

        :return:
        """
        self.Model.clear()

    def removeHighLightRows(self):
        """

        :return:
        """
        pass

    def selected_body_column_index(self, withData: bool = False):
        """

        :param withData:
        :return:
        """
        column = self.currentIndex().column()
        columnName = self.Model.headerData(column, Qt.Horizontal)
        if withData:
            data = []
            for row in range(self.Model.rowCount()):
                data.append(self.itemAt(row, column))

            return column, columnName, data
        else:
            return column, None, None

    def clear_filter(self):
        """

        :return:
        """
        self.filter("", None)
        return len(self._all_rows())

    def filter(self, inputStr, searchColumns=None, reverse=False):
        """
        Filter source in TableViews, when user input words in filter.
        :param inputStr:
        :param searchColumns:
        :param reverse:
        :return:
        """
        row_items = self._all_rows()
        columnCount = self.Model.columnCount()

        match_count = 0

        if inputStr != "":
            for item in row_items:
                self.hideRow(item.row())

            for item in row_items:
                if searchColumns:
                    row = " ".join([str(self.itemAt(item.row(), x)) for x in searchColumns])
                else:
                    row = " ".join([str(self.itemAt(item.row(), x)) for x in range(columnCount)])

                chinese = row
                initials = Chinese.allInitials(row)
                # print(inputStr, inputStr.upper(), chinese, initials)

                patten = re.search(inputStr, chinese, re.M | re.I) or re.search(inputStr.upper(), initials, re.M | re.I)

                if reverse:
                    if not patten:
                        self.showRow(item.row())
                        # print(inputStr, chinese, initials)
                        match_count += 1
                else:
                    if patten:
                        self.showRow(item.row())
                        # print(inputStr, chinese, initials)
                        match_count += 1

            return match_count
        else:
            for item in row_items:
                self.showRow(item.row())

            match_count = len(row_items)
            return match_count

    def sumOfColumn(self, column_idx: int):
        """

        :param column_idx:
        :return:
        """
        row_items = self._all_rows()

        column_sum = 0.0

        for item in row_items:
            column_value = self.itemAt(item.row(), column_idx)
            if column_value and Utils.isANumber(column_value):
                column_sum += float(column_value)

        return round(column_sum, 2)

    def set_numeric_column_color(self):
        """

        :return:
        """
        pass

    def set_column_foreground_color(self, base_column_index: int, colored_column: int):
        """
        Set the color of the column whose contents are numbers.
        :param base_column_index:
        :param colored_column:
        :return:
        """
        model = self.model()
        for row in range(model.rowCount()):
            if model.index(row, base_column_index).data():
                data = model.index(row, base_column_index).data()
                if Utils.isANumber(data):
                    if float(data) < 0:
                        color = QColor('green')
                    elif float(data) == 0.00:
                        color = QColor('black')
                    else:
                        color = QColor('red')
                    model.item(row, colored_column).setForeground(color)

    def set_column_background_color(self, color: QColor, base_column_index: int, colored_column: int):
        """

        :param color:
        :param base_column_index:
        :param colored_column:
        :return:
        """
        model = self.model()
        for row in range(model.rowCount()):
            if model.index(row, base_column_index).data():
                data = model.index(row, base_column_index).data()
                if Utils.isANumber(data):
                    if float(data) < 0:
                        color = QColor('#BFEFFF')

                    model.item(row, colored_column).setBackground(color)

    def hide_blank_rows(self, hide):
        """

        :param hide:
        :return:
        """
        rowList = self._all_rows()
        if not hide:
            for row in range(self.Model.rowCount()):
                rowList[row].setEnabled(True)
                self.showRow(row)
        else:
            for row in range(self.Model.rowCount()):
                for column in range(1, self.Model.columnCount()):
                    if self.Model.index(row, column).data() == "":
                        # print(row, column, self.__model.index(row, column).data(), True)
                        self.Model.item(row).setCheckState(Qt.Unchecked)
                        rowList[row].setEnabled(False)
                        self.hideRow(row)
                        break

    def checked_row(self):
        """

        :return:
        """
        rowList = self._all_rows()
        for idx, item in enumerate(rowList):
            if item.checkState() == Qt.Checked:
                return idx

        return -1

    def exportImage(self, imagePath):
        """

        :param imagePath:
        :return:
        """
        self.clearSelection()
        image = self.grab(self.rect())
        image.save(imagePath)

    def length(self):
        """

        :return:
        """
        return len(list(self.Model.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive)))

    def _all_rows(self):
        """
        Get all rows in this table.
        :return:
        """
        return list(self.Model.findItems("*", Qt.MatchWildcard | Qt.MatchRecursive))

    def _set_all_rows_check_state(self, state):
        """
        Inner function, set check status of all rows.
        :param state:
        :return:
        """
        rowList = self._all_rows()

        for item in rowList:
            self.Model.item(item.row()).setCheckState(state)

        return self._has_row_checked()

    def _set_selected_rows_check_state(self, selectedItemList, checkState):
        """
        Inner function, set check status of the rows which were selected by user.
        :param checkState:
        :return:
        """
        # collect selected rows, use set to remove duplicated rows
        rowIndexSet = set()
        for selectedCell in selectedItemList:
            rowIndexSet.add(selectedCell.row())

        allRows = self._all_rows()

        for row, item in enumerate(allRows):
            if row in rowIndexSet:
                self.Model.item(row).setCheckState(checkState)

        return self._has_row_checked()

    def _set_selected_state_by_key(self, column, key, state):
        """
        Inner function, set check status of the rows which contain the key and were selected by user.
        :param state:
        :return:
        """
        rowList = self._all_rows()

        for row, item in enumerate(rowList):
            if self.itemAt(row, column).find(key) != -1:
                self.Model.item(row).setCheckState(state)

        return self._has_row_checked()

    def _set_selected_state_by_row(self, rowIndex, state):
        """
        Inner function, set check status of the rows which contain the key and were selected by user.
        :param state:
        :return:
        """

        self.Model.item(rowIndex).setCheckState(state)

        return self._has_row_checked()

    def _has_row_checked(self):
        """
        Go through all cells, find .
        :return:
        """
        rowList = self._all_rows()
        for item in rowList:
            if item.checkState() == Qt.Checked:
                return True

        return False


class TableCellItem(QStandardItem):
    """
    Table Cell Item class, user defined __lt__, __eq__ and __gt__ method, in order to sort column.
    """

    def __init__(self, data):
        super().__init__(data)

    def __lt__(self, other):
        try:
            return Utils.number_value_of(self.text()) < Utils.number_value_of(other.text())
        except ValueError as e:
            print(e)

    def __eq__(self, other):
        try:
            return Utils.number_value_of(self.text()) == Utils.number_value_of(other.text())
        except ValueError as e:
            print(e)

    def __gt__(self, other):
        try:
            return Utils.number_value_of(self.text()) > Utils.number_value_of(other.text())
        except ValueError as e:
            print(e)
