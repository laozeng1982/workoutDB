import os

import pandas as pd
from PyQt5.QtWidgets import QMessageBox

from datamodel.Action import Equipment, BodyPart, Action
from windows.widgets.ActionFormBase import ActionFormBase
from windows.widgets.ActionFormCnWidgetUI import Ui_ActionFormCnWidget

Equipment = Equipment()
BodyPart = BodyPart()


class ActionFormCnWidget(ActionFormBase, Ui_ActionFormCnWidget):
    def __init__(self, parent):
        super(ActionFormCnWidget, self).__init__(parent)
        self.setupUi(self)

        self.equipmentCmbBox.addItems(Equipment.cnlist())
        self.bodyPartCmbBox.addItems(BodyPart.cnlist())
        self.excelPath = "D:/gym-visual/baseDataCn.xlsx"

    def setAction(self, action):
        # set edit
        translate = False
        if action.Id:
            # action was read from excel
            readAction = Action()
            readAction.readActionById(self.excelPath, action.Id)
            if readAction.Id:
                action = readAction
            else:
                translate = True
        else:
            translate = True

        if translate:
            # action was read from web
            self.bodyPartCmbBox.setCurrentText(BodyPart.findCnBy(action.part))
            self.equipmentCmbBox.setCurrentText(Equipment.findCnBy(action.equipment))
        else:
            self.bodyPartCmbBox.setCurrentText(action.part)
            self.equipmentCmbBox.setCurrentText(action.equipment)

        self.nameEdit.setText(action.name)
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

    def saveExcel(self, actionId, imageFile, instructionImageFile, gifFile):
        action = self.collectAction(imageFile, instructionImageFile, gifFile)
        if action and actionId > 0:
            action.Id = actionId
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
                        else:
                            return
                    else:
                        # add a new one
                        df = dataFrame.append(action.toDf(), sort=False, ignore_index=True)
                        df.to_excel(self.excelPath, index=False)
                        return action.Id
                else:
                    action.toDf().to_excel(self.excelPath, index=False)

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            return
