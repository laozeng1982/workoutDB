#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# author: JianGe, created on: 2018/10/15

import datetime
import json
import math
import os
import platform
import re
import shutil
import sys
from json import JSONDecodeError

import win32api
from PyQt5.QtWidgets import QFileDialog

from utilities.DateTimeHelper import StdDateFormat
from utilities.LogHelper import logger


def selectDirectory(parent, caption, path, component=None):
    """
    Select directory to parent widget
    :param parent: parent widget which contains a browse button.
    :param caption: title of dialog.
    :param path: the default path where to start
    :param component: when user select a folder, set this component's text to the folder.
    :return:
    """
    selectedDirectory = QFileDialog.getExistingDirectory(parent, caption=caption, directory=path)

    if selectedDirectory == "":
        print("\nSelect Directory Canceled!")
        pass
    else:
        # print("\n你选择的文件夹为:", selectedDirectory)
        if component:
            component.setText(selectedDirectory)

    return selectedDirectory


def selectFile(parent, title, path, component, isOpen, filters='', initialFilter=''):
    """
    Select file to parent widget
    :param parent: parent widget which contains a browse button.
    :param title: dialog title.
    :param path: the default path where to start.
    :param component: when user select a folder, set this component's text to the folder.
    :param isOpen:
    :param filters:
    :param initialFilter:
    :return:
    """
    if isOpen:
        selectedFile = QFileDialog.getOpenFileName(parent, title, path, filter=filters, initialFilter=initialFilter)[0]
    else:
        selectedFile = QFileDialog.getSaveFileName(parent, title, path, filter=filters, initialFilter=initialFilter)[0]

    if selectedFile == "":
        print("\nSelect File Canceled!")
        pass
    else:
        # print("\n你选择的文件夹为:", files)
        if component:
            component.setText(selectedFile)

    return selectedFile


def selectFiles(parent, title, path, filters='', initialFilter=''):
    """
    Select files to parent widget
    :param parent: parent widget which contains a browse button.
    :param title: dialog title.
    :param path: the default path where to start.
    :param filters:
    :param initialFilter:
    :return:
    """
    selectedFiles = QFileDialog.getOpenFileNames(parent, title, path, filter=filters, initialFilter=initialFilter)[0]

    if selectedFiles == "":
        print("\nSelect Files Canceled!")
        return None
    else:
        return selectedFiles


def isContainChinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def isRunningInChineseDirectory():
    print(os.path.abspath('.'))
    return isContainChinese(os.path.abspath('.'))


def _is_equal(obj1, obj2, printDiff=False):
    """
    Recursive function to compare two objects, and return results.
    :param obj1:
    :param obj2:
    :param printDiff:
    :return:
    """
    returnInfo = {"result": True, "info": ""}
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        len1 = len(obj1.keys())
        len2 = len(obj2.keys())
        if len1 != len2:
            returnInfo["result"] = False
            returnInfo["info"] = "'s len1 = " + str(len1) + ", " + "len2 = " + str(len2)
            if printDiff:
                print(returnInfo["info"])
            return returnInfo
        for key in obj1:
            if key not in obj2:
                returnInfo["result"] = False
                returnInfo["info"] = "['" + key + "']" + " not found in para2" + str(obj2.keys())
                if printDiff:
                    print(returnInfo["info"])
                return returnInfo
            else:
                value1 = obj1[key]
                value2 = obj2[key]
                returnInfoSub = _is_equal(value1, value2)
                returnInfo["result"] = returnInfo["result"] and returnInfoSub["result"]
                if not returnInfoSub["result"]:
                    returnInfo["info"] = "['" + key + "']" + returnInfoSub["info"]
                    if printDiff:
                        print(returnInfo["info"])
                    return returnInfo

    elif isinstance(obj1, list) and isinstance(obj2, list):
        len1 = len(obj1)
        len2 = len(obj2)
        if len1 != len2:
            returnInfo["result"] = False
            returnInfo["info"] = "'s len1 = " + str(len1) + ", " + "len2 = " + str(len2)
            if printDiff:
                print(returnInfo["info"])
            return returnInfo
        for i in range(len1):
            value1 = obj1[i]
            value2 = obj2[i]
            returnInfoSub = _is_equal(value1, value2)
            returnInfo["result"] = returnInfo["result"] and returnInfoSub["result"]
            if not returnInfoSub["result"]:
                returnInfo["info"] = "[" + str(i) + "]" + returnInfoSub["info"]
                if printDiff:
                    print(returnInfo["info"])
                return returnInfo

    else:
        returnInfo["result"] = (obj1 == obj2)
        if not returnInfo["result"]:
            returnInfo["info"] = ":" + str(obj1) + " not equal " + str(obj2)
            if printDiff:
                print(returnInfo["info"])
        return returnInfo

    return returnInfo


def is_equal(obj1, obj2, printDiff=False):
    """

    :param obj1:
    :param obj2:
    :param printDiff:
    :return:
    """
    returnInfo = _is_equal(obj1, obj2, printDiff)

    return returnInfo['result']


def has_this_element(element, source):
    """

    :param element:
    :param source:
    :return:
    """
    hasThisElement = False
    for item in source:
        # print(element)
        # print(item)
        # print('\n')
        if is_equal(element, item):
            hasThisElement = True
            break

    return hasThisElement


def number_value_of(aString):
    """
    Get the value of a string.
    :param aString:
    :return:
    """
    if isANumber(aString):
        if aString.isdigit():
            return int(aString)
        else:
            return float(aString)
    else:
        return aString


def isANumber(num):
    """

    :param num:
    :return:
    """
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    matched = True

    for item in str(num).split('.'):
        matched = matched and pattern.match(item)

    return matched


def round_to(number, index=4):
    if not math.isnan(number):
        return round(number, index)


def formatNumber(number):
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)


def format_date(dt):
    if isinstance(dt, datetime.datetime):
        return dt.strftime(StdDateFormat)
    else:
        if isinstance(dt, str) and len(dt) == 8:
            return datetime.datetime.strptime(dt, "%Y%m%d").strftime(StdDateFormat)


def btn_check(btn_name: str, btn):
    return re.search(btn_name, btn.objectName()) is not None


def transfer_docs2_list(foundDocs):
    rows = []
    if foundDocs:
        for doc in foundDocs:
            row = []
            for item in doc:
                row.append(doc[item])
            rows.append(row)

    return rows


def load_json(file_path):
    contents = {}
    try:
        if file_path:
            # logger.info("find position file at: %s" % position_file_path)
            with open(file_path, mode='r', encoding='UTF-8') as fp:
                contents = json.load(fp)
        else:
            logger.info("cant find position file at: %s" % file_path)
    except FileNotFoundError and TypeError and JSONDecodeError as e:
        logger.error(e)
    finally:
        return contents


def dump_json(json_data, file_path):
    try:
        with open(file_path, mode='w+', encoding='UTF-8') as fp:
            json.dump(json_data, fp, indent=4, ensure_ascii=False)
    except FileNotFoundError and TypeError as e:
        logger.error(e)


def openFile(filePath):
    if sys.platform == "win32" or platform.system() == "Windows":
        win32api.ShellExecute(0, 'open', filePath, "", "", 1)
    else:
        os.system(filePath)


def copyFile(source, target):
    """

    :param source:
    :param target:
    :return:
    """
    try:
        shutil.copy(source, target)
        return True
    except Exception as e:
        logger.error(e)
        return False


def splitRowBy(row: str, separator):
    """
    Split a str by separator into a str array.
    1. Strip first
    2. then replace '\t' by space.
    3. then remove redundant space, and split it.
    :param row:
    :param separator:
    :return:
    """
    return re.sub(' +', ' ', row.strip().replace("\t", " ")).split(separator)


# Entry for testing
if __name__ == "__main__":
    # exact_bars_from_binary('D:\\new_zx_allin1\\vipdoc\sh\lday\\sh600000.day')
    # exact_bars_from_binary('D:\\new_zx_allin1\\vipdoc\sh\\fzline\\sh600000.lc5')
    # compare_binary_ascii()

    print(sys.platform, type(sys.platform))
    print(platform.system(), type(platform.system()))
    dt1 = datetime.datetime.now()

    print(type(dt1) == datetime.datetime)
    print(isinstance(dt1, datetime.datetime))

    print(format_date("19910403"))
