"""

"""
import os

import pandas as pd

import BaseTools
from datamodel.Data import DataTable


def saveExercises():
    try:
        filePath = ".\\ExerciseDataEnglish.xlsx"
        if os.path.exists(filePath):
            dataFrame = pd.read_excel(filePath, encoding='utf-8')
            print(dataFrame)
            if not dataFrame.empty:
                BaseTools.save(dataFrame, DataTable.Exercises)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    saveExercises()
