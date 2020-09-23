import os

import pandas as pd
from PyQt5.QtWidgets import QMessageBox

from datamodel.Action import Equipment, BodyPart, Action
from windows.widgets.ActionFormBase import ActionFormBase
from windows.widgets.ActionFormEnWidgetUI import Ui_ActionFormEnWidget

baseDir = "D:/gym-visual"
excelPath = baseDir + "/baseData.xlsx"


class ActionFormEnWidget(ActionFormBase, Ui_ActionFormEnWidget):
    def __init__(self, parent):
        super(ActionFormEnWidget, self).__init__(parent)
        self.setupUi(self)

        self.Parent = parent

        self.equipmentCmbBox.addItems(Equipment().enlist())
        self.bodyPartCmbBox.addItems(BodyPart().enlist())
        self.excelPath = "D:/gym-visual/baseDataEn.xlsx"

    def setAction(self, action: Action):
        self.bodyPartCmbBox.setCurrentText(action.part)
        self.nameEdit.setText(action.name)
        self.equipmentCmbBox.setCurrentText(action.equipment)
        self.targetMusleEdit.setText(action.target)
        self.synergistsEdit.setText(action.synergists)
        self.importantStabilizersEdit.setText(action.importantStabilizers)
        self.dynamicStabilizersEdit.setText(action.dynamicStabilizers)
        self.mechanicsEdit.setText(action.mechanics)
        self.forceEdit.setText(action.force)
        self.groupQuantitySBox.setValue(int(action.groupQuantity))
        self.quantityPerGroupSBox.setValue(int(action.quantityPerGroup))
        self.quantityPerActionSBox.setValue(int(action.quantityPerAction))
        self.unitCmbBox.setCurrentText(action.actionUom)
        self.startPositionTextEdit.setPlainText(action.startingPosition)
        self.executionTextEdit.setPlainText(action.execution)
        self.commentsTextEdit.setPlainText(action.commentsTips)

        self.currentAction = action

    def selectEquipment(self, equipment):
        """

        :param equipment:
        :return:
        """
        print("equipment:", equipment)
        self.Parent.onChangeEnEquipment(Equipment().findCnBy(equipment))

    def selectBodyPart(self, bodyPart):
        """

        :param bodyPart:
        :return:
        """
        print("bodyPart:", bodyPart)
        print("find:", BodyPart().findEnBy(bodyPart))
        self.Parent.onChangeEnBodyPart(BodyPart().findCnBy(bodyPart))

    def saveExcel(self, imageFile, instructionImageFile, gifFile):
        action = self.collectAction(imageFile, instructionImageFile, gifFile)
        if self.currentAction.Id:
            action.Id = int(self.currentAction.Id)
        if action:
            try:
                # if True:
                if os.path.exists(self.excelPath):
                    dataFrame = pd.read_excel(self.excelPath)
                    # print(dataFrame)
                    namelist = list(dataFrame['name'])
                    if action.name in namelist:
                        # replace
                        reply = QMessageBox.question(self, "Replace", "Already has this english action.\n"
                                                                      "Click 'Yes' to replace, 'No' to Cancel.",
                                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                        if reply == QMessageBox.Yes:
                            idx = namelist.index(action.name)
                            df = dataFrame[0:idx].append(action.toDf()).append(dataFrame[idx + 1:])
                            df.to_excel(self.excelPath, index=False)
                            return action.Id
                        else:
                            return -1
                    else:
                        # add a new one
                        action.Id = len(dataFrame) + 1
                        df = dataFrame.append(action.toDf(), sort=False, ignore_index=True)
                        df.to_excel(self.excelPath, index=False)
                        return action.Id
                else:
                    action.Id = 1
                    action.toDf().to_excel(self.excelPath, index=False)

                    return 1

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                return -1
        else:
            return -1
