import os

import pandas as pd

from utilities.LogHelper import logger


class Item(object):
    def __init__(self, idx: int, english: str, chinese: str, value=None):
        """

        :type idx: int
        :param idx:
        :param english:
        :param chinese:
        :param value:
        """
        self.Id = idx
        self.English = english
        self.Chinese = chinese
        self.Value = value


class Base(object):
    def __init__(self):
        self.UnKnown = Item(0, "UnKnown", u"未知")

    def enlist(self):
        items = [x for x in vars(self).values() if isinstance(x, Item)]
        # print(items)
        enList = [x.English for x in items]
        # print(enList)
        return enList

    def cnlist(self):
        items = [x for x in vars(self).values() if isinstance(x, Item)]
        # print(items)
        cnList = [x.Chinese for x in items]
        # print(cnList)
        return cnList

    def findCnBy(self, en):
        for item in vars(self).values():
            if isinstance(item, Item) and item.English == en:
                return item.Chinese

    def findEnBy(self, cn):
        for item in vars(self).values():
            if isinstance(item, Item) and item.Chinese == cn:
                return item.English


class Action(object):
    def __init__(self):
        self.Id = None
        self.part = " "
        self.name = " "
        self.equipment = " "
        self.target = " "
        self.synergists = " "
        self.importantStabilizers = " "
        self.dynamicStabilizers = " "
        self.mechanics = " "
        self.force = " "
        self.groupQuantity = 6
        self.quantityPerGroup = 10
        self.quantityPerAction = 10
        self.actionUom = " "
        self.startingPosition = " "
        self.execution = " "
        self.commentsTips = " "
        self.imageFile = " "
        self.instructionImageFile = " "
        self.gifFile = " "

    def set(self, name, value):
        try:
            if name == 'Id':
                self.__setattr__(name, int(value))
            else:
                self.__setattr__(name, str(value))
        except:
            self.__setattr__(name, "")

    def toString(self):
        for key in vars(self).keys():
            print("%s: %s" % (key, vars(self).get(key)))

    def headList(self):
        # print(list(vars(self).keys()))
        return list(vars(self).keys())

    def valueList(self):
        # print(list(vars(self).values()))
        return [[x] for x in vars(self).values()]

    def toDf(self):
        df = pd.DataFrame()
        for key in vars(self).keys():
            df[key] = [vars(self).get(key)]

        return df

    def readActionByName(self, excelPath, actionName):
        if os.path.exists(excelPath):
            try:
                df = pd.read_excel(excelPath)
                if len(df) >= 0:
                    row = list(df['name']).index(actionName)
                    for column in df.columns:
                        self.set(column, df[column][row])

            except Exception as e:
                logger.error(e)
        else:
            logger.error("%s not exist!!!" % excelPath)

    def readActionById(self, excelPath, actionId):
        if os.path.exists(excelPath):
            try:
                df = pd.read_excel(excelPath)
                if len(df) >= 0:
                    row = list(df['Id']).index(int(actionId))
                    for column in df.columns:
                        self.set(column, df[column][row])

            except Exception as e:
                logger.error(e)
        else:
            logger.error("%s not exist!!!" % excelPath)


class Equipment(Base):
    def __init__(self):
        """

        """
        super(Equipment, self).__init__()

        # 自由器械
        self.Band = Item(1, "Band", u"弹力带")
        self.BattlingRope = Item(2, "Battling Rope", u"战绳")
        self.Barbell = Item(3, "Barbell", u"杠铃")
        self.Bench = Item(4, "Bench", u"平板")
        self.BenchPress = Item(5, "Bench Press", u"卧推架")
        self.Freehand = Item(6, "Freehand", u"徒手")
        self.BosuBall = Item(7, "Bosu Ball", u"波速球")
        self.Cable = Item(8, "Cable", u"拉索")
        self.Dumbbell = Item(9, "Dumbbell", u"哑铃")
        self.Hammer = Item(10, "Hammer", u"战锤")
        self.KettleBell = Item(11, "Kettle bell", u"壶铃")
        self.MedicineBall = Item(12, "Medicine Ball", u"药球")
        self.StabilityBall = Item(13, "Stability Ball", u"平衡球")
        self.SuspensionRope = Item(14, "Suspension Rope", u"悬挂绳")
        self.TRXRope = Item(15, "TRX Rope", u"TRX绳")
        self.WheelRoller = Item(16, "Wheel Roller", u"健腹轮")

        # 固定器械
        self.GantryTrainingFrame = Item(17, "Gantry Train Frame", u"龙门架")
        self.SmithMachine = Item(18, "Smith Machine", u"史密斯机")
        self.BenchPressMachine = Item(19, "Bench Press Machine", u"推胸机")
        self.HummerMachine = Item(20, "Hummer Machine", u"悍马机")

        self.ButterflyMachine = Item(21, "Butterfly Machine", u"蝴蝶机")  # 夹胸肌
        self.RowingMachine = Item(22, "Rowing Machine", u"划船机")
        self.PulldownMachine = Item(23, "Pulldown Machine", u"下拉机")
        self.LandmineRack = Item(24, "Landmine Rack", u"地雷架")  #

        self.ShoulderPressMachine = Item(25, "Shoulder Press Machine", u"下拉机")
        self.LegPressMachine = Item(26, "Leg Press Machine", u"倒蹬机")
        self.HackMachine = Item(27, "Hack Machine", u"哈克机")
        self.LegCurlMachine = Item(28, "Leg Curl Machine", u"腿弯举机")

        self.SeatedLegExtensionsMachine = Item(29, "Seated Leg Extensions Machine", u"坐姿腿屈伸机")
        self.CalfRaiseMachine = Item(30, "Calf Raise Machine", u"提踵机")
        self.HorizontalBar = Item(31, "Horizontal Bar", u"单杠")
        self.ParallelBars = Item(32, "Parallel Bars", u"双杠")

        self.SitUpBench = Item(33, "Sit Up Bench", u"仰卧板")
        self.RomanChair = Item(34, "Roman Chair", u"罗马椅")
        self.PreacherChair = Item(35, "Preacher Chair", u"牧师椅")
        self.Trendmill = Item(36, "Trendmill", u"跑步机")
        self.Bicycling = Item(37, "Bicycling", u"动感单车")
        self.RecumbentBike = Item(38, "Recumbent Bike", u"卧式动感单车")
        self.ClimberMachine = Item(39, "Climber Machine", u"登山机")


class BodyPart(Base):
    def __init__(self):
        super(BodyPart, self).__init__()
        self.Cardio = Item(1, "Cardio", u"有氧")
        self.Stretching = Item(2, "Stretching", u"拉伸")
        self.Pilates = Item(3, "Pilates", u"普拉提")
        self.Yoga = Item(4, "Yoga", u"瑜伽")
        self.Plyometrics = Item(5, "Plyometrics", u"增强式训练")  # 增强式训练

        self.Composite = Item(6, "Composite", u"复合训练")

        self.Neck = Item(7, "Neck", u"颈部")  # 颈部
        self.Shoulders = Item(8, "Shoulders", u"肩部")  # 肩部

        self.Chest = Item(9, "Chest", u"胸部")  # 胸部
        self.Back = Item(10, "Back", u"背部")  # 背部

        self.Abdomen = Item(11, "Abdomen", u"腹部")  # 腹部
        self.Waist = Item(12, "Waist", u"腰部")  # 腰部

        self.Hips = Item(13, "Hips", u"臀部")  # 臀部

        self.UpperArms = Item(14, "UpperArms", u"上臂")  # 上臂
        self.ForeArms = Item(15, "ForeArms", u"小臂")  # 小臂
        self.Wrist = Item(16, "Wrist", u"手腕")  # 手腕

        self.Thighs = Item(17, "Thighs", u"大腿")  # 大腿
        self.Calves = Item(18, "Calves", u"小腿")  # 小腿


if __name__ == '__main__':
    print(BodyPart().enlist())
    print(BodyPart().cnlist())

    print(BodyPart().findCnBy("Cardio"))
    print(BodyPart().findEnBy(u"背部"))
