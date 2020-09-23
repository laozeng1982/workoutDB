import ctypes
import os

import pandas as pd
from PyQt5.QtCore import QModelIndex, QStringListModel
from PyQt5.QtGui import QIcon, QPixmap, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QSystemTrayIcon

from DownloadGvmPictures import findRightDriver
from datamodel.Action import Action, Equipment
from datamodel.Action import BodyPart
from utilities.LogHelper import logger
from windows.ActionsCollectorWindowUI import Ui_ActionsCollectorMainWindow
from windows.ActionsDataTableView import ActionsDataTableView
from windows.progress.ProgressWindow import ProgressWindow, UserThread
from windows.widgets.ActionFormCnWidget import ActionFormCnWidget
from windows.widgets.ActionFormEnWidget import ActionFormEnWidget
from windows.widgets.ImageViewWidget import ImageViewWidget

baseDir = "D:/gym-visual"
BaseEnglishExcelPath = baseDir + "/baseDataEn.xlsx"


class ActionsCollectorWindow(QMainWindow, Ui_ActionsCollectorMainWindow):
    """
    Create position window, including path setting and default system setting.
    """

    def __init__(self, parent=None):
        super(ActionsCollectorWindow, self).__init__(parent)
        self.setupUi(self)

        self.isExit = False
        self.webDriver = findRightDriver()
        self.currentEquipment = None
        self.currentBodyPart = None
        self.currentAction = Action()

        self.trayIconMenu = QMenu(self)
        self.trayIcon = QSystemTrayIcon(self)

        self.statusBar().showMessage('Ready')

        self.setIcon()
        self.addSystemTray()

        self.show()
        self.webDriver.get("https://weighttraining.guide/")

        self.enActionForm = ActionFormEnWidget(self)
        self.cnActionForm = ActionFormCnWidget(self)
        self.englishGBox.layout().addWidget(self.enActionForm)
        self.chineseGBox.layout().addWidget(self.cnActionForm)

        self.tableView = ActionsDataTableView(self)
        self.tableGLayout.addWidget(self.tableView)

        self.briefImageView = ImageViewWidget(None)
        self.briefGLayout.addWidget(self.briefImageView)

        self.gifImageView = ImageViewWidget(None)
        self.gifGLayout.addWidget(self.gifImageView)

        self.instructionImageView = ImageViewWidget(None)
        self.instructionGLayout.addWidget(self.instructionImageView)

        self.equipmentCmbBox.addItems(Equipment().cnlist())
        self.bodyPartCmbBox.addItems(BodyPart().cnlist())

        self.initData()

    def initData(self):
        if os.path.exists(BaseEnglishExcelPath):
            df = pd.read_excel(BaseEnglishExcelPath)
            headers = list(df.columns)
            # print(headers)
            rows = list(df.values)
            # print(rows)

            # self.tableView.initialize(headers, rows)

            nameList = list(df['name'])
            slm = QStringListModel()
            # set data to model
            slm.setStringList(sorted(nameList))
            # bind mode to listView
            self.listView.setModel(slm)

    def addSystemTray(self):
        """
        add a system tray
        :return:
        """
        minimizeAction = QAction("Minimize", self, triggered=self.hide)
        maximizeAction = QAction("Maximize", self, triggered=self.showMaximized)
        restoreAction = QAction("Restore", self, triggered=self.showNormal)
        exitAction = QAction("Exit", self, triggered=self.exit)

        self.trayIconMenu.addAction(minimizeAction)
        self.trayIconMenu.addAction(maximizeAction)
        self.trayIconMenu.addAction(restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(exitAction)

        self.trayIcon.setIcon(QIcon(".\\images\\run.png"))
        self.trayIcon.setContextMenu(self.trayIconMenu)
        # set double click action
        self.trayIcon.activated[QSystemTrayIcon.ActivationReason].connect(self.activateIcon)
        self.trayIcon.show()

    def activateIcon(self, reason):
        """
        double click action
        :param reason:
        :return:
        """

        if reason == QSystemTrayIcon.DoubleClick:
            if self.isMinimized():
                self.raise_()
                self.show()
            else:
                if self.isHidden():
                    self.raise_()
                    self.show()
                else:
                    self.hide()

    def setIcon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(".\\images\\run.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

    def exit(self):
        self.close()

    def changeLanguage(self, btn):
        print(btn.objectName())

    def readFromWeb(self):
        """
        Read data from web
        :return:
        """
        progressWindow = ProgressWindow(self, "Reading", self.processResults)
        progressWindow.exec()

    def processResults(self, thread: UserThread):
        """
        Process reading results and initialize an action.
        :param thread:
        :return:
        """
        action = Action()
        if thread:
            thread.percentageTrigger.emit(50)
        if len(self.webDriver.find_elements_by_tag_name("h1")) > 0:
            actionName = self.webDriver.find_elements_by_tag_name("h1")[0]
            action.name = actionName.get_property("textContent").strip()

        contents = self.webDriver.find_elements_by_class_name("entry-content")
        if len(contents) > 0:
            text = contents[0].get_property("outerText")
            # print(text.split("\n"))

            lines = text.split("\n")
            startPositionIdx = 0
            executionIdx = 0
            commentsIdx = 0
            endContentsIdx = 0
            for idx, line in enumerate(lines):
                if line.startswith("Target muscle:"):
                    action.target = line.replace("Target muscle: ", "")

                if line.startswith("Target muscles:"):
                    action.target = line.replace("Target muscles: ", "")

                if line.startswith("Synergists:"):
                    action.synergists = line.replace("Synergists: ", "")

                if line.startswith("Dynamic stabilizer:"):
                    action.dynamicStabilizers = line.replace("Dynamic stabilizer: ", "")

                if line.startswith("Dynamic stabilizers:"):
                    action.dynamicStabilizers = line.replace("Dynamic stabilizers: ", "")

                if line.startswith("Important stabilizer:"):
                    action.importantStabilizers = line.replace("Important stabilizer: ", "")

                if line.startswith("Important stabilizers"):
                    action.importantStabilizers = line.replace("Important stabilizers: ", "")

                if line.startswith("Mechanics:"):
                    action.mechanics = line.replace("Mechanics: ", "")

                if line.startswith("Force:"):
                    action.force = line.replace("Force: ", "")

                if line.startswith("Starting position"):
                    startPositionIdx = idx

                if line.startswith("Execution"):
                    executionIdx = idx

                if line.startswith("Comments and tips"):
                    commentsIdx = idx

                if 'video' in line:
                    endContentsIdx = idx - 1
                    break

            action.startingPosition = "\n".join(lines[startPositionIdx + 1: executionIdx])
            action.execution = "\n".join(lines[executionIdx + 1: commentsIdx])
            action.commentsTips = "\n".join(lines[commentsIdx + 1: endContentsIdx])

        # action.toString()
        if thread:
            thread.percentageTrigger.emit(100)
        self.currentAction = action
        self.setAction()

    def setAction(self):
        """

        :return:
        """

        # set edit
        self.enActionForm.setAction(self.currentAction)
        self.cnActionForm.setAction(self.currentAction)

        # find picture and
        filterName = "-".join(self.currentAction.name.split(" ")).lower()

        file = baseDir + "/jpg" + "/" + self.currentAction.imageFile
        if self.currentAction.imageFile.strip() and os.path.exists(file):
            self.briefImageView.setPath(file)
        else:
            hasJpg = False
            for file in os.listdir(baseDir + "/jpg"):
                if filterName in file.lower():
                    self.briefImageView.setPath(baseDir + "/jpg" + "/" + file)
                    hasJpg = True
                    break

            if not hasJpg:
                self.briefImageView.setPath(baseDir + "/jpg" + "/" + filterName + ".jpg")

        file = baseDir + "/gif" + "/" + self.currentAction.gifFile
        if self.currentAction.gifFile.strip() and os.path.exists(file):
            self.gifImageView.setPath(file)
        else:
            hasGif = False
            for file in os.listdir(baseDir + "/gif"):
                if filterName in file.lower():
                    self.gifImageView.setPath(baseDir + "/gif" + "/" + file)
                    hasGif = True
                    break

            if not hasGif:
                self.gifImageView.setPath(baseDir + "/gif" + "/" + filterName + ".gif")

        file = baseDir + "/png" + "/" + self.currentAction.instructionImageFile
        if self.currentAction.instructionImageFile.strip() and os.path.exists(file):
            self.instructionImageView.setPath(file)
        else:
            hasPng = False
            for file in os.listdir(baseDir + "/png"):
                if filterName in file.lower():
                    self.instructionImageView.setPath(baseDir + "/png" + "/" + file)
                    hasPng = True
                    break

            if not hasPng:
                self.instructionImageView.setPath(baseDir + "/png" + "/" + filterName + ".png")

    def saveExcel(self):
        imageFile = os.path.basename(self.briefImageView.imagePathEdit.text())
        instructionImageFile = os.path.basename(self.instructionImageView.imagePathEdit.text())
        gifFile = os.path.basename(self.gifImageView.imagePathEdit.text())
        actionId = self.enActionForm.saveExcel(imageFile, instructionImageFile, gifFile)
        self.cnActionForm.saveExcel(actionId, imageFile, instructionImageFile, gifFile)
        self.initData()

    def onChangeEnEquipment(self, equipment):
        """

        :param equipment:
        :return:
        """
        if hasattr(self, 'cnActionForm'):
            self.cnActionForm.equipmentCmbBox.setCurrentText(equipment)

    def onChangeEnBodyPart(self, bodyPart):
        """

        :param bodyPart:
        :return:
        """
        if hasattr(self, 'cnActionForm'):
            self.cnActionForm.bodyPartCmbBox.setCurrentText(bodyPart)

    def selectEquipment(self, equipment):
        """

        :param equipment:
        :return:
        """
        print("equipment:", equipment)
        self.filterBy(equipment=equipment)
        print("find:", Equipment().findEnBy(equipment))

    def selectBodyPart(self, bodyPart):
        """

        :param bodyPart:
        :return:
        """
        print("bodyPart:", bodyPart)
        print("find:", BodyPart().findEnBy(bodyPart))
        self.filterBy(bodyPart=bodyPart)
        # self.equipmentCmbBox.setCurrentText(BodyPart().findEnBy(bodyPart))

    def filterBy(self, equipment=None, bodyPart=None):
        """

        :param equipment:
        :param bodyPart:
        :return:
        """
        if not equipment:
            equipment = self.currentEquipment
        else:
            self.currentEquipment = equipment

        if not bodyPart:
            bodyPart = self.currentBodyPart
        else:
            self.currentBodyPart = bodyPart

        # df = pd.read_excel(excelPath)

    def selectAction(self, qModelIndex: QModelIndex):
        selectedActionName = self.listView.model().data(qModelIndex, 0)
        logger.info("selected: %3d, %s" % (qModelIndex.row(), selectedActionName))
        action = Action()
        action.readActionByName(BaseEnglishExcelPath, selectedActionName)
        # df = pd.read_excel(BaseEnglishExcelPath)
        # for column in df.columns:
        #     action.set(column, df[column][qModelIndex.row()])

        # print(qModelIndex.row(), action.toString())
        self.currentAction = action
        self.setAction()

    def onActionSelected(self, action: Action):
        self.currentAction = action
        self.setAction()

    def exportJson(self):
        pass

    def translate(self):
        pass

    def sync(self):
        pass

    def rename(self):
        pass

    def closeEvent(self, event: QCloseEvent) -> None:
        self.webDriver.close()


def capitalizeFile():
    for file in os.listdir(baseDir + "/jpg"):
        fileName = "-".join([x.capitalize() for x in file.split('-')])
        # print(file, fileName)
        print(file)
        print(fileName)
        os.rename(baseDir + "/jpg/" + file, baseDir + "/jpg/" + fileName)

    for file in os.listdir(baseDir + "/gif"):
        fileName = "-".join([x.capitalize() for x in file.split('-')])
        print(file)
        print(fileName)
        os.rename(baseDir + "/gif/" + file, baseDir + "/gif/" + fileName)

    for file in os.listdir(baseDir + "/png"):
        fileName = "-".join([x.capitalize() for x in file.split('-')])
        print(file)
        print(fileName)
        os.rename(baseDir + "/png/" + file, baseDir + "/png/" + fileName)


if __name__ == '__main__':
    a = Action()
    a.headList()
    a.valueList()

    df1 = a.toDf().append(a.toDf())
    df2 = a.toDf().append(a.toDf()).append(a.toDf()).append(a.toDf())
    # df.append(a.toDf())
    print(df2)
    capitalizeFile()
    # try:
    #     excelPath = baseDir + "/baseData.xlsx"
    #     if os.path.exists(excelPath):
    #         dataFrame = pd.read_excel(excelPath)
    #         print(dataFrame)
    #         df = dataFrame.append(a.toDf(), sort=False, ignore_index=True)
    #         df.to_excel(excelPath, index=False)
    #     else:
    #         a.toDf().to_excel(excelPath, index=False)
    # except Exception as e:
    #     QMessageBox.critical(None, "Error", str(e))
