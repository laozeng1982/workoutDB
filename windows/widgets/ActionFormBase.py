from PyQt5.QtWidgets import QWidget, QMessageBox

from datamodel.Action import Action


class ActionFormBase(QWidget):
    def __init__(self, parent):
        super(ActionFormBase, self).__init__(parent)
        self.excelPath = ""
        self.currentAction = None

    def setAction(self, action: Action):

        # set edit
        # TODO
        pass

    def collectAction(self, imageFile, instructionImageFile, gifFile):
        if self.nameEdit.text().strip():
            action = Action()
            action.part = self.bodyPartCmbBox.currentText()
            action.name = self.nameEdit.text()
            action.equipment = self.equipmentCmbBox.currentText()
            action.target = self.targetMusleEdit.text()
            action.synergists = self.synergistsEdit.text()
            action.importantStabilizers = self.importantStabilizersEdit.text()
            action.dynamicStabilizers = self.dynamicStabilizersEdit.text()
            action.mechanics = self.mechanicsEdit.text()
            action.force = self.forceEdit.text()
            action.groupQuantity = self.groupQuantitySBox.value()
            action.quantityPerGroup = self.quantityPerGroupSBox.value()
            action.quantityPerAction = self.quantityPerActionSBox.value()
            action.actionUom = self.unitCmbBox.currentText()
            action.startingPosition = self.startPositionTextEdit.toPlainText()
            action.execution = self.executionTextEdit.toPlainText()
            action.commentsTips = self.commentsTextEdit.toPlainText()

            action.imageFile = imageFile
            action.instructionImageFile = instructionImageFile
            action.gifFile = gifFile

            return action
        else:
            QMessageBox.critical(self, "Error", "Please fill name.")
            return None

    # def saveExcel(self, isEnglish, imageFile, instructionImageFile, gifFile):
    #     pass
