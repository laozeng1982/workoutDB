import json
import os
import shutil
import time

from utilities.File import safeRemove, md5List

lastVersion = "2.27.1"
currentVersion = "2.27.2"


def runInstall():
    # beforeCompile()
    runCompile()
    # afterCompile()


def beforeCompile():
    """
    Operations before compile.
    :return:
    """
    safeRemove(".\\build\\GameHelper")
    safeRemove(".\\dist\\GameHelperOld")

    if os.path.exists(".\\dist\\GameHelper"):
        os.rename(".\\dist\\GameHelper", ".\\dist\\GameHelperOld")


def afterCompile():
    safeRemove(".\\dist\\GameHelper\\config\\running.log")
    safeRemove(".\\dist\\GameHelper\\config\\passwd.json")
    shutil.copy(".\\config\\passwd2.json", ".\\dist\\GameHelper\\config\\passwd.json")

    with open(".\\dist\\redundant_files.dat", "r") as fp:
        files = fp.readlines()
        for file in files:
            file_path = os.path.join(".\\dist\\GameHelper", file.strip())
            print(file_path)
            safeRemove(file_path)

        # delete Qt files
        safeRemove(".\\dist\\GameHelper\\PyQt5\\Qt\\qml")

        for file in os.listdir(".\\dist\\GameHelper\\PyQt5\\Qt\\translations"):
            file_path = os.path.join(".\\dist\\GameHelper\\PyQt5\\Qt\\translations", file.strip())
            if file.endswith('.qm'):
                safeRemove(file_path)

    updateFiles = checkUpdatedFiles()
    if len(updateFiles) >= 0:
        for file in updateFiles:
            shutil.copy(os.path.join(file.get('root'), file.get('name')),
                        os.path.join(".\\dist\\updates", file.get('name')))
        updateInfo = {
            "name": "GameHelper",
            "version": currentVersion,
            "updates": updateFiles
        }

        try:
            with open(os.path.join(".\\dist\\updates", "update.json"), mode='w+', encoding='UTF-8') as fp:
                json.dump(updateInfo, fp, indent=4, ensure_ascii=False)
        except FileNotFoundError and TypeError as e:
            print(e)


def runCompile():
    os.system("pyinstaller --win-private-assemblies ActionsCollector.spec")


def checkUpdatedFiles():
    oldPath = ".\\dist\\GameHelperOld"
    newPath = ".\\dist\\GameHelper"

    start = time.time()
    oldList = md5List(oldPath)
    newList = md5List(newPath)

    updateFiles = []
    idx = 1
    for newFile in newList:
        if newFile not in oldList:
            print("new file %4d: %s" % (idx, newFile))
            updateFiles.append(newFile)
            idx += 1

    end = time.time()
    print("Spend: %s seconds!" % (end - start))

    return updateFiles


if __name__ == '__main__':
    runInstall()
