import codecs
import hashlib
import math
import os
import shutil

import chardet
import filetype
import numpy
import pandas as pd
import xlrd
from pandas import Series

from utilities import Utils
from utilities.LogHelper import logger
from windows.progress.ProgressWindow import UserThread


class FileInfo(object):
    def __init__(self, filePath, checkMd5=False):
        self.Path = filePath  # full path of this file
        self.Name = os.path.basename(filePath)  # file name
        self.Type = "Binary" if isBinaryFile(filePath) else "Text"
        if checkMd5:
            self.Md5 = md5Of(filePath)
        else:
            self.Md5 = None
        kind = filetype.guess(filePath)
        if kind is not None:
            # print('Cannot guess file type!')
            self.Extension = kind.extension
            self.MIME = kind.mime
        else:
            self.Extension = filePath.split(".")[-1]
            self.MIME = "Unknown"

        self.Same = False

    def md5(self):
        self.Md5 = md5Of(self.Path)

    def sameAs(self, path):
        return self.Md5 == md5Of(path)

    def toString(self):
        sList = []
        for key, item in zip(vars(self).keys(), vars(self).values()):
            sList.append("%-10s: %s\n" % (key, item))

        print("".join(sList))
        return "".join(sList)

    def toDict(self):
        return {
            'FilePath': self.Path,
            'FileName': self.Name,
            'Md5sum': self.Md5,
            'Extension': self.Extension,
            'MIME': self.MIME,
            'Same': False
        }


def safeRemove(filePath):
    if os.path.exists(filePath):
        if os.path.isdir(filePath):
            shutil.rmtree(filePath, True)
        else:
            os.remove(filePath)


def md5List(path):
    idx = 1
    md5_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            fullPath = os.path.join(root, name)
            if os.path.isfile(fullPath):
                md5 = md5Of(fullPath)
                tmp = {
                    'root': root.replace('Old', '').replace("dist\\\\", ""),
                    'name': name,
                    # 'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'size': str(math.ceil(os.path.getsize(fullPath) / 1024)),
                    'md5': md5
                }
                # print("%4d: %s" % (idx, tmp))
                md5_list.append(tmp)
                idx += 1

    return md5_list


def md5Of(filename):
    """
    Calculate md5sum of given file.

    According to test, 8096 bytes has better performance.
    For 20 GBs binary data,
        on linux system md5sum cost 39 seconds;
        on same windows system,
        using 8096 cost 43 seconds,
        using 1048576 (1024 * 1024) cost 221 seconds,
        using 1073741824 (1024 * 1024 * 1024) cost 594 seconds.

    :param filename:
    :return:
    """
    if not os.path.isfile(filename):
        return None

    try:
        myHash = hashlib.md5()
        with open(filename, 'rb') as fp:
            while True:
                b = fp.read(8096)
                if b:
                    myHash.update(b)
                else:
                    break
            fp.close()

        return myHash.hexdigest()
    except Exception as e:
        logger.error(e)
        return None


def isBinaryFile(filePath):
    """
    Detect a file according to it's text bom.
    :param filePath: file name with absolute path.
    :return: True or False, True mean is a binary file.
    :param filePath:
    :return:
    """

    TEXT_BOMS = (
        codecs.BOM_UTF16_BE,
        codecs.BOM_UTF16_LE,
        codecs.BOM_UTF32_BE,
        codecs.BOM_UTF32_LE,
        codecs.BOM_UTF8,
    )
    try:
        with open(filePath, 'rb') as file:
            CHUNKSIZE = 8192
            initial_bytes = file.read(CHUNKSIZE)
            file.close()
        #: BOMs to indicate that a file is a text file even if it contains zero bytes.
        isBin = not any(initial_bytes.startswith(bom) for bom in TEXT_BOMS) and b'\0' in initial_bytes

        # logger.info(isBin)
        return isBin
    except Exception as e:
        logger.error(e)
        return False


def listDirectories(path1, path2, thread: UserThread = None):
    """
    Compare files in two directories.
    :param path1:
    :param path2:
    :param thread:
    :return:
    """
    # 1. walk through directory to gather all basic info
    filesList = []
    totalFiles = 0
    for path in [path1, path2]:
        infoList = {
            'Parent': path,
            'FileList': []
        }
        for root, dirs, files in os.walk(path):
            for file in files:
                md5info = {
                    'FilePath': os.path.join(root, file),
                    'FileName': file,
                    'Md5sum': '',
                    'Same': False
                }
                infoList['FileList'].append(md5info)
                totalFiles += 1

        filesList.append(infoList)

    idx = 1
    # 2. split walk in directories in order to get progress info because md5sum may need much longer time.
    if totalFiles > 0:
        for path in filesList:
            for item in path['FileList']:
                item['Md5sum'] = md5Of(item['FilePath'])

                if thread:
                    thread.percentageTrigger.emit(idx * 100 / totalFiles)
                idx += 1
                # print(item)

        path1List = filesList[0]['FileList']
        path2List = filesList[1]['FileList']
        print('-' * 120)
        print("%s has %s items" % (filesList[0]['Parent'], len(path1List)))
        print("%s has %s items\n" % (filesList[1]['Parent'], len(path2List)))

        # compare base on md5sum
        for item1 in path1List:
            for item2 in path2List:
                # if item1.get('FileName') == item2.get('FileName') or item1.get('Md5sum') == item2.get('Md5sum'):
                if item1.get('Md5sum') == item2.get('Md5sum'):
                    item1['Same'] = True
                    item2['Same'] = True
                    break

        if thread:
            thread.resultsTrigger.emit(filesList)


def listFilesInfo(path1, path2, thread: UserThread = None):
    """
    List information of two files.
    :param path1:
    :param path2:
    :param thread:
    :return:
    """
    infoList = []
    idx = 1
    for path in [path1, path2]:
        kind = filetype.guess(path)
        if kind is not None:
            Extension = kind.extension
            MIME = kind.mime
        else:
            # logger.info('Cannot guess file type!')
            Extension = path.split(".")[-1]
            MIME = "Unknown"
        info = {
            'File Path': path,
            'File Type': "Binary" if isBinaryFile(path) else "Text",
            'Md5': md5Of(path),
            'Extension': Extension,
            'MIME': MIME
        }
        if thread:
            thread.percentageTrigger.emit(50 * idx)
        idx += 1

        infoList.append(info)

    thread.resultsTrigger.emit(infoList)


def detectEncoding(filePath: str):
    """
    Detect the encoding of a file.
    :param filePath:
    :return:
    """
    encoding = "utf-8"
    try:
        with open(filePath, mode='rb') as fp:
            encoding = chardet.detect(fp.read(100)).get('encoding')
    except Exception as e:
        logger.error(e)
    finally:
        # print(encoding)
        return encoding


def readRows(filePath: str, rowCount: int):
    """
    Read text file by row, and return certain number of rows.
    :param filePath:
    :param rowCount: if rowCount < file row number, return array with length rowCount, else return all rows.
    :return:
    """
    try:
        rows = []
        if os.path.isfile(filePath):
            with open(filePath, 'r', encoding=detectEncoding(filePath)) as fp:

                idx = 0
                while idx < rowCount:
                    line = fp.readline()
                    if not line:
                        # end of file, return ""
                        break
                    # remove blank row by strip()
                    if line.strip():
                        rows.append(line)
                        idx += 1

        return rows
    except Exception as e:
        logger.error(e)
        return []


def readData(filePath, separator):
    """

    :param filePath:
    :param separator:
    :return:
    """
    # read data
    data = []
    df = pd.DataFrame()
    curveNameRow = 0
    dataStartRow = 0
    maxColumnCount = 0

    if filePath:
        if isBinaryFile(filePath):
            if filePath.endswith('.xls') or filePath.endswith('.xlsx'):
                excel_file = xlrd.open_workbook(filePath)
                sheet = excel_file.sheet_by_index(0)

                for idx in range(sheet.nrows):
                    row = sheet.row_values(idx)
                    if "#" in row:
                        row.remove("#")

                    if "dep" in row.lower() or "dept" in row.lower() or "depth" in row.lower():
                        curveNameRow = idx + 2
                        dataStartRow = idx + 3
                    data.append(row)
        else:
            rows = readRows(filePath, 100000)

            for idx, row in enumerate(rows):
                newRow = Utils.splitRowBy(row, separator)
                if "#" in newRow:
                    newRow.remove("#")

                if "dep" in row.lower() or "dept" in row.lower() or "depth" in row.lower():
                    curveNameRow = idx + 1
                    dataStartRow = idx + 2

                if "EOD" in row:
                    break
                data.append(newRow)
                maxColumnCount = max(maxColumnCount, len(newRow))

    if data:
        # make a DataFrame with fixed column name for locate data in the following steps.
        columns = ["Column %s" % (x + 1) for x in range(maxColumnCount)]
        df = pd.DataFrame(data=data, columns=columns)
        # print(df)

    return data, df, curveNameRow, dataStartRow


def toFloat(series: Series, nullValue):
    """
    Convert a series of string to float, if string means null, replace with numpy.nan.
    :param series:
    :param nullValue:
    :return:
    """
    newList = []
    for item in series:
        try:
            if item:
                value = float(item)
                if value == float(nullValue):
                    value = numpy.nan
            else:
                value = numpy.nan
        except (ValueError, TypeError) as e:
            logger.error(e)
            value = numpy.nan
        newList.append(value)

    return newList


def modify():
    for file in os.listdir("D:\\md5test\\test3"):
        with open(os.path.join("D:\\md5test\\test3", file), 'w', encoding='gb2312') as fp:
            lines = fp.readlines()
            lines.append("abcdefg")
            fp.writelines(lines)


def binaryTest():
    path = os.path.expanduser("~")
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file, ":", isBinaryFile(os.path.join(root, file)))


if __name__ == '__main__':
    # binaryTest()
    pass
