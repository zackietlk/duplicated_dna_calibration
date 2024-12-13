import contextlib
import json
import os
from os import environ
from sys import path as syspath
from sys import platform

# if you use Maya, use absolute path
ROOT_DIR = "D:/work/MetaHuman-DNA-Calibration"
WORK_DIR = "D:/work/UnrealFest"

MAYA_VERSION = "2022"  # or 2023
ROOT_LIB_DIR = f"{ROOT_DIR}/lib/Maya{MAYA_VERSION}"
if platform == "win32":
    LIB_DIR = f"{ROOT_LIB_DIR}/windows"
elif platform == "linux":
    LIB_DIR = f"{ROOT_LIB_DIR}/linux"
else:
    raise OSError(
        "OS not supported, please compile dependencies and add value to LIB_DIR"
    )
DATA_DIR = f"{ROOT_DIR}/data"

# Add bin directory to maya plugin path
if "MAYA_PLUG_IN_PATH" in environ:
    separator = ":" if platform == "linux" else ";"
    environ["MAYA_PLUG_IN_PATH"] = separator.join([environ["MAYA_PLUG_IN_PATH"], LIB_DIR])
else:
    environ["MAYA_PLUG_IN_PATH"] = LIB_DIR

surface_joints = ['FACIAL_C_NeckB', 'FACIAL_L_NeckB1', 'FACIAL_R_NeckB1', 'FACIAL_L_NeckB2', 'FACIAL_R_NeckB2',
                  'FACIAL_C_12IPV_NeckB1', 'FACIAL_C_12IPV_NeckB2', 'FACIAL_L_12IPV_NeckB3', 'FACIAL_R_12IPV_NeckB3',
                  'FACIAL_L_12IPV_NeckB4', 'FACIAL_R_12IPV_NeckB4', 'FACIAL_L_12IPV_NeckB5', 'FACIAL_R_12IPV_NeckB5',
                  'FACIAL_L_12IPV_NeckB6', 'FACIAL_R_12IPV_NeckB6', 'FACIAL_L_12IPV_NeckB7', 'FACIAL_R_12IPV_NeckB7',
                  'FACIAL_C_NeckBackB', 'FACIAL_L_NeckBackB', 'FACIAL_R_NeckBackB', 'FACIAL_C_12IPV_NeckBackB1',
                  'FACIAL_C_12IPV_NeckBackB2', 'FACIAL_L_12IPV_NeckBackB1', 'FACIAL_R_12IPV_NeckBackB1',
                  'FACIAL_L_12IPV_NeckBackB2', 'FACIAL_R_12IPV_NeckBackB2', 'FACIAL_C_AdamsApple',
                  'FACIAL_C_12IPV_AdamsA1', 'FACIAL_C_12IPV_AdamsA2', 'FACIAL_L_NeckA1', 'FACIAL_R_NeckA1',
                  'FACIAL_L_NeckA2', 'FACIAL_R_NeckA2', 'FACIAL_L_NeckA3', 'FACIAL_R_NeckA3', 'FACIAL_L_12IPV_NeckA1',
                  'FACIAL_R_12IPV_NeckA1', 'FACIAL_L_12IPV_NeckA2', 'FACIAL_R_12IPV_NeckA2', 'FACIAL_L_12IPV_NeckA3',
                  'FACIAL_R_12IPV_NeckA3', 'FACIAL_L_12IPV_NeckA4', 'FACIAL_R_12IPV_NeckA4', 'FACIAL_L_12IPV_NeckA5',
                  'FACIAL_R_12IPV_NeckA5', 'FACIAL_L_12IPV_NeckA6', 'FACIAL_R_12IPV_NeckA6', 'FACIAL_C_NeckBackA',
                  'FACIAL_L_NeckBackA', 'FACIAL_R_NeckBackA', 'FACIAL_C_12IPV_NeckBackA1', 'FACIAL_C_12IPV_NeckBackA2',
                  'FACIAL_L_12IPV_NeckBackA1', 'FACIAL_R_12IPV_NeckBackA1', 'FACIAL_L_12IPV_NeckBackA2',
                  'FACIAL_R_12IPV_NeckBackA2', 'FACIAL_C_Hair1', 'FACIAL_L_12IPV_Hair1', 'FACIAL_R_12IPV_Hair1',
                  'FACIAL_C_Hair2', 'FACIAL_C_Hair3', 'FACIAL_C_Hair4', 'FACIAL_C_Hair5', 'FACIAL_C_Hair6',
                  'FACIAL_L_HairA1', 'FACIAL_R_HairA1', 'FACIAL_L_HairA2', 'FACIAL_R_HairA2', 'FACIAL_L_HairA3',
                  'FACIAL_R_HairA3', 'FACIAL_L_HairA4', 'FACIAL_R_HairA4', 'FACIAL_L_HairA5', 'FACIAL_R_HairA5',
                  'FACIAL_L_HairA6', 'FACIAL_R_HairA6', 'FACIAL_L_HairB1', 'FACIAL_R_HairB1', 'FACIAL_L_HairB2',
                  'FACIAL_R_HairB2', 'FACIAL_L_HairB3', 'FACIAL_R_HairB3', 'FACIAL_L_HairB4', 'FACIAL_R_HairB4',
                  'FACIAL_L_HairB5', 'FACIAL_R_HairB5', 'FACIAL_L_Temple', 'FACIAL_R_Temple', 'FACIAL_L_12IPV_Temple1',
                  'FACIAL_R_12IPV_Temple1', 'FACIAL_L_12IPV_Temple2', 'FACIAL_R_12IPV_Temple2',
                  'FACIAL_L_12IPV_Temple3', 'FACIAL_R_12IPV_Temple3', 'FACIAL_L_12IPV_Temple4',
                  'FACIAL_R_12IPV_Temple4', 'FACIAL_L_HairC1', 'FACIAL_R_HairC1', 'FACIAL_L_HairC2', 'FACIAL_R_HairC2',
                  'FACIAL_L_HairC3', 'FACIAL_R_HairC3', 'FACIAL_L_HairC4', 'FACIAL_R_HairC4', 'FACIAL_L_Sideburn1',
                  'FACIAL_R_Sideburn1', 'FACIAL_L_Sideburn2', 'FACIAL_R_Sideburn2', 'FACIAL_L_Sideburn3',
                  'FACIAL_R_Sideburn3', 'FACIAL_L_Sideburn4', 'FACIAL_R_Sideburn4', 'FACIAL_L_Sideburn5',
                  'FACIAL_R_Sideburn5', 'FACIAL_L_Sideburn6', 'FACIAL_R_Sideburn6', 'FACIAL_C_ForeheadSkin',
                  'FACIAL_L_ForeheadInSkin', 'FACIAL_R_ForeheadInSkin', 'FACIAL_L_12IPV_ForeheadSkin1',
                  'FACIAL_R_12IPV_ForeheadSkin1', 'FACIAL_L_12IPV_ForeheadSkin2', 'FACIAL_R_12IPV_ForeheadSkin2',
                  'FACIAL_L_12IPV_ForeheadSkin3', 'FACIAL_R_12IPV_ForeheadSkin3', 'FACIAL_L_12IPV_ForeheadSkin4',
                  'FACIAL_R_12IPV_ForeheadSkin4', 'FACIAL_L_12IPV_ForeheadSkin5', 'FACIAL_R_12IPV_ForeheadSkin5',
                  'FACIAL_L_12IPV_ForeheadSkin6', 'FACIAL_R_12IPV_ForeheadSkin6', 'FACIAL_L_ForeheadMidSkin',
                  'FACIAL_R_ForeheadMidSkin', 'FACIAL_L_ForeheadOutSkin', 'FACIAL_R_ForeheadOutSkin',
                  'FACIAL_C_Forehead1', 'FACIAL_L_Forehead1', 'FACIAL_R_Forehead1', 'FACIAL_C_Forehead2',
                  'FACIAL_L_Forehead2', 'FACIAL_R_Forehead2', 'FACIAL_C_Forehead3', 'FACIAL_L_Forehead3',
                  'FACIAL_R_Forehead3', 'FACIAL_C_12IPV_Forehead1', 'FACIAL_L_12IPV_Forehead1',
                  'FACIAL_R_12IPV_Forehead1', 'FACIAL_C_12IPV_Forehead2', 'FACIAL_L_12IPV_Forehead2',
                  'FACIAL_R_12IPV_Forehead2', 'FACIAL_C_12IPV_Forehead3', 'FACIAL_L_12IPV_Forehead3',
                  'FACIAL_R_12IPV_Forehead3', 'FACIAL_C_12IPV_Forehead4', 'FACIAL_L_12IPV_Forehead4',
                  'FACIAL_R_12IPV_Forehead4', 'FACIAL_C_12IPV_Forehead5', 'FACIAL_L_12IPV_Forehead5',
                  'FACIAL_R_12IPV_Forehead5', 'FACIAL_C_12IPV_Forehead6', 'FACIAL_L_12IPV_Forehead6',
                  'FACIAL_R_12IPV_Forehead6', 'FACIAL_L_ForeheadInA1', 'FACIAL_L_ForeheadInA2', 'FACIAL_L_ForeheadInA3',
                  'FACIAL_L_ForeheadInB1', 'FACIAL_L_ForeheadInB2', 'FACIAL_L_12IPV_ForeheadIn1',
                  'FACIAL_L_12IPV_ForeheadIn2', 'FACIAL_L_12IPV_ForeheadIn3', 'FACIAL_L_12IPV_ForeheadIn4',
                  'FACIAL_L_12IPV_ForeheadIn5', 'FACIAL_L_12IPV_ForeheadIn6', 'FACIAL_L_12IPV_ForeheadIn7',
                  'FACIAL_L_12IPV_ForeheadIn8', 'FACIAL_L_12IPV_ForeheadIn9', 'FACIAL_L_12IPV_ForeheadIn10',
                  'FACIAL_L_12IPV_ForeheadIn11', 'FACIAL_L_12IPV_ForeheadIn12', 'FACIAL_L_12IPV_ForeheadIn13',
                  'FACIAL_L_12IPV_ForeheadIn14', 'FACIAL_R_ForeheadInA1', 'FACIAL_R_ForeheadInA2',
                  'FACIAL_R_ForeheadInA3', 'FACIAL_R_ForeheadInB1', 'FACIAL_R_ForeheadInB2',
                  'FACIAL_R_12IPV_ForeheadIn1', 'FACIAL_R_12IPV_ForeheadIn2', 'FACIAL_R_12IPV_ForeheadIn3',
                  'FACIAL_R_12IPV_ForeheadIn5', 'FACIAL_R_12IPV_ForeheadIn4', 'FACIAL_R_12IPV_ForeheadIn6',
                  'FACIAL_R_12IPV_ForeheadIn7', 'FACIAL_R_12IPV_ForeheadIn8', 'FACIAL_R_12IPV_ForeheadIn9',
                  'FACIAL_R_12IPV_ForeheadIn10', 'FACIAL_R_12IPV_ForeheadIn12', 'FACIAL_R_12IPV_ForeheadIn11',
                  'FACIAL_R_12IPV_ForeheadIn13', 'FACIAL_R_12IPV_ForeheadIn14', 'FACIAL_L_ForeheadMid1',
                  'FACIAL_L_ForeheadMid2', 'FACIAL_L_12IPV_ForeheadMid15', 'FACIAL_L_12IPV_ForeheadMid16',
                  'FACIAL_L_12IPV_ForeheadMid17', 'FACIAL_L_12IPV_ForeheadMid18', 'FACIAL_L_12IPV_ForeheadMid19',
                  'FACIAL_L_12IPV_ForeheadMid20', 'FACIAL_L_12IPV_ForeheadMid21', 'FACIAL_L_12IPV_ForeheadMid22',
                  'FACIAL_R_ForeheadMid1', 'FACIAL_R_ForeheadMid2', 'FACIAL_R_12IPV_ForeheadMid15',
                  'FACIAL_R_12IPV_ForeheadMid16', 'FACIAL_R_12IPV_ForeheadMid17', 'FACIAL_R_12IPV_ForeheadMid18',
                  'FACIAL_R_12IPV_ForeheadMid19', 'FACIAL_R_12IPV_ForeheadMid20', 'FACIAL_R_12IPV_ForeheadMid21',
                  'FACIAL_R_12IPV_ForeheadMid22', 'FACIAL_L_ForeheadOutA1', 'FACIAL_L_ForeheadOutA2',
                  'FACIAL_L_ForeheadOutB1', 'FACIAL_L_ForeheadOutB2', 'FACIAL_L_12IPV_ForeheadOut23',
                  'FACIAL_L_12IPV_ForeheadOut24', 'FACIAL_L_12IPV_ForeheadOut25', 'FACIAL_L_12IPV_ForeheadOut26',
                  'FACIAL_L_12IPV_ForeheadOut27', 'FACIAL_L_12IPV_ForeheadOut28', 'FACIAL_L_12IPV_ForeheadOut29',
                  'FACIAL_L_12IPV_ForeheadOut30', 'FACIAL_L_12IPV_ForeheadOut31', 'FACIAL_L_12IPV_ForeheadOut32',
                  'FACIAL_R_ForeheadOutA1', 'FACIAL_R_ForeheadOutA2', 'FACIAL_R_ForeheadOutB1',
                  'FACIAL_R_ForeheadOutB2', 'FACIAL_R_12IPV_ForeheadOut23', 'FACIAL_R_12IPV_ForeheadOut24',
                  'FACIAL_R_12IPV_ForeheadOut25', 'FACIAL_R_12IPV_ForeheadOut26', 'FACIAL_R_12IPV_ForeheadOut27',
                  'FACIAL_R_12IPV_ForeheadOut28', 'FACIAL_R_12IPV_ForeheadOut29', 'FACIAL_R_12IPV_ForeheadOut30',
                  'FACIAL_R_12IPV_ForeheadOut31', 'FACIAL_R_12IPV_ForeheadOut32', 'FACIAL_L_12IPV_EyesackU0',
                  'FACIAL_R_12IPV_EyesackU0', 'FACIAL_L_EyesackUpper1', 'FACIAL_L_EyesackUpper2',
                  'FACIAL_L_EyesackUpper3', 'FACIAL_R_EyesackUpper1', 'FACIAL_R_EyesackUpper2',
                  'FACIAL_R_EyesackUpper3', 'FACIAL_L_EyesackUpper4', 'FACIAL_R_EyesackUpper4',
                  'FACIAL_L_EyelidUpperFurrow1', 'FACIAL_L_EyelidUpperFurrow2', 'FACIAL_L_EyelidUpperFurrow3',
                  'FACIAL_R_EyelidUpperFurrow1', 'FACIAL_R_EyelidUpperFurrow2', 'FACIAL_R_EyelidUpperFurrow3',
                  'FACIAL_L_EyelidUpperB1', 'FACIAL_L_EyelidUpperB2', 'FACIAL_L_EyelidUpperB3',
                  'FACIAL_R_EyelidUpperB1', 'FACIAL_R_EyelidUpperB2', 'FACIAL_R_EyelidUpperB3',
                  'FACIAL_L_EyelidUpperA1', 'FACIAL_L_EyelashesUpperA1', 'FACIAL_L_EyelidUpperA2',
                  'FACIAL_L_EyelashesUpperA2', 'FACIAL_L_EyelidUpperA3', 'FACIAL_L_EyelashesUpperA3',
                  'FACIAL_R_EyelidUpperA1', 'FACIAL_R_EyelashesUpperA1', 'FACIAL_R_EyelidUpperA2',
                  'FACIAL_R_EyelashesUpperA2', 'FACIAL_R_EyelidUpperA3', 'FACIAL_R_EyelashesUpperA3',
                  'FACIAL_L_EyelidLowerA1', 'FACIAL_L_EyelidLowerA2', 'FACIAL_L_EyelidLowerA3',
                  'FACIAL_R_EyelidLowerA1', 'FACIAL_R_EyelidLowerA2', 'FACIAL_R_EyelidLowerA3',
                  'FACIAL_L_EyelidLowerB1', 'FACIAL_L_EyelidLowerB2', 'FACIAL_L_EyelidLowerB3',
                  'FACIAL_R_EyelidLowerB1', 'FACIAL_R_EyelidLowerB2', 'FACIAL_R_EyelidLowerB3',
                  'FACIAL_L_EyeCornerInner1', 'FACIAL_L_EyeCornerInner2', 'FACIAL_R_EyeCornerInner1',
                  'FACIAL_R_EyeCornerInner2', 'FACIAL_L_EyeCornerOuter1', 'FACIAL_L_EyelashesCornerOuter1',
                  'FACIAL_L_EyeCornerOuter2', 'FACIAL_R_EyeCornerOuter1', 'FACIAL_R_EyelashesCornerOuter1',
                  'FACIAL_R_EyeCornerOuter2', 'FACIAL_L_12IPV_EyeCornerO1', 'FACIAL_R_12IPV_EyeCornerO1',
                  'FACIAL_L_12IPV_EyeCornerO2', 'FACIAL_R_12IPV_EyeCornerO2', 'FACIAL_L_EyesackLower1',
                  'FACIAL_L_EyesackLower2', 'FACIAL_L_12IPV_EyesackL1', 'FACIAL_L_12IPV_EyesackL2',
                  'FACIAL_L_12IPV_EyesackL3', 'FACIAL_L_12IPV_EyesackL4', 'FACIAL_L_12IPV_EyesackL5',
                  'FACIAL_L_12IPV_EyesackL6', 'FACIAL_L_12IPV_EyesackL7', 'FACIAL_L_12IPV_EyesackL8',
                  'FACIAL_R_EyesackLower1', 'FACIAL_R_EyesackLower2', 'FACIAL_R_12IPV_EyesackL1',
                  'FACIAL_R_12IPV_EyesackL2', 'FACIAL_R_12IPV_EyesackL3', 'FACIAL_R_12IPV_EyesackL4',
                  'FACIAL_R_12IPV_EyesackL5', 'FACIAL_R_12IPV_EyesackL6', 'FACIAL_R_12IPV_EyesackL7',
                  'FACIAL_R_12IPV_EyesackL8', 'FACIAL_L_CheekInner1', 'FACIAL_L_CheekInner2', 'FACIAL_L_CheekInner3',
                  'FACIAL_L_CheekInner4', 'FACIAL_R_CheekInner1', 'FACIAL_R_CheekInner2', 'FACIAL_R_CheekInner3',
                  'FACIAL_R_CheekInner4', 'FACIAL_L_CheekOuter1', 'FACIAL_L_CheekOuter2', 'FACIAL_L_CheekOuter3',
                  'FACIAL_R_CheekOuter1', 'FACIAL_R_CheekOuter2', 'FACIAL_R_CheekOuter3', 'FACIAL_L_CheekOuter4',
                  'FACIAL_R_CheekOuter4', 'FACIAL_L_12IPV_CheekOuter1', 'FACIAL_R_12IPV_CheekOuter1',
                  'FACIAL_L_12IPV_CheekOuter2', 'FACIAL_R_12IPV_CheekOuter2', 'FACIAL_L_12IPV_CheekOuter3',
                  'FACIAL_R_12IPV_CheekOuter3', 'FACIAL_L_12IPV_CheekOuter4', 'FACIAL_R_12IPV_CheekOuter4',
                  'FACIAL_C_12IPV_NoseBridge1', 'FACIAL_L_12IPV_NoseBridge1', 'FACIAL_R_12IPV_NoseBridge1',
                  'FACIAL_C_12IPV_NoseBridge2', 'FACIAL_L_12IPV_NoseBridge2', 'FACIAL_R_12IPV_NoseBridge2',
                  'FACIAL_L_NoseBridge', 'FACIAL_R_NoseBridge', 'FACIAL_C_NoseUpper', 'FACIAL_L_NoseUpper',
                  'FACIAL_R_NoseUpper', 'FACIAL_C_12IPV_NoseUpper1', 'FACIAL_C_12IPV_NoseUpper2',
                  'FACIAL_L_12IPV_NoseUpper1', 'FACIAL_R_12IPV_NoseUpper1', 'FACIAL_L_12IPV_NoseUpper2',
                  'FACIAL_R_12IPV_NoseUpper2', 'FACIAL_L_12IPV_NoseUpper3', 'FACIAL_R_12IPV_NoseUpper3',
                  'FACIAL_L_12IPV_NoseUpper4', 'FACIAL_R_12IPV_NoseUpper4', 'FACIAL_L_12IPV_NoseUpper5',
                  'FACIAL_R_12IPV_NoseUpper5', 'FACIAL_L_12IPV_NoseUpper6', 'FACIAL_R_12IPV_NoseUpper6',
                  'FACIAL_L_NasolabialBulge1', 'FACIAL_R_NasolabialBulge1', 'FACIAL_L_12IPV_NasolabialB13',
                  'FACIAL_R_12IPV_NasolabialB13', 'FACIAL_L_12IPV_NasolabialB14', 'FACIAL_R_12IPV_NasolabialB14',
                  'FACIAL_L_12IPV_NasolabialB15', 'FACIAL_R_12IPV_NasolabialB15', 'FACIAL_L_NasolabialBulge2',
                  'FACIAL_L_NasolabialBulge3', 'FACIAL_L_12IPV_NasolabialB1', 'FACIAL_L_12IPV_NasolabialB2',
                  'FACIAL_L_12IPV_NasolabialB3', 'FACIAL_L_12IPV_NasolabialB4', 'FACIAL_L_12IPV_NasolabialB5',
                  'FACIAL_L_12IPV_NasolabialB6', 'FACIAL_L_12IPV_NasolabialB7', 'FACIAL_L_12IPV_NasolabialB8',
                  'FACIAL_L_12IPV_NasolabialB9', 'FACIAL_L_12IPV_NasolabialB10', 'FACIAL_L_12IPV_NasolabialB11',
                  'FACIAL_L_12IPV_NasolabialB12', 'FACIAL_R_NasolabialBulge2', 'FACIAL_R_NasolabialBulge3',
                  'FACIAL_R_12IPV_NasolabialB1', 'FACIAL_R_12IPV_NasolabialB2', 'FACIAL_R_12IPV_NasolabialB3',
                  'FACIAL_R_12IPV_NasolabialB4', 'FACIAL_R_12IPV_NasolabialB5', 'FACIAL_R_12IPV_NasolabialB6',
                  'FACIAL_R_12IPV_NasolabialB7', 'FACIAL_R_12IPV_NasolabialB8', 'FACIAL_R_12IPV_NasolabialB9',
                  'FACIAL_R_12IPV_NasolabialB10', 'FACIAL_R_12IPV_NasolabialB11', 'FACIAL_R_12IPV_NasolabialB12',
                  'FACIAL_L_NasolabialFurrow', 'FACIAL_R_NasolabialFurrow', 'FACIAL_L_12IPV_NasolabialF1',
                  'FACIAL_R_12IPV_NasolabialF1', 'FACIAL_L_12IPV_NasolabialF2', 'FACIAL_R_12IPV_NasolabialF2',
                  'FACIAL_L_12IPV_NasolabialF3', 'FACIAL_R_12IPV_NasolabialF3', 'FACIAL_L_12IPV_NasolabialF4',
                  'FACIAL_R_12IPV_NasolabialF4', 'FACIAL_L_12IPV_NasolabialF5', 'FACIAL_R_12IPV_NasolabialF5',
                  'FACIAL_L_12IPV_NasolabialF6', 'FACIAL_R_12IPV_NasolabialF6', 'FACIAL_L_12IPV_NasolabialF7',
                  'FACIAL_R_12IPV_NasolabialF7', 'FACIAL_L_12IPV_NasolabialF8', 'FACIAL_R_12IPV_NasolabialF8',
                  'FACIAL_L_12IPV_NasolabialF9', 'FACIAL_R_12IPV_NasolabialF9', 'FACIAL_L_CheekLower1',
                  'FACIAL_L_CheekLower2', 'FACIAL_L_12IPV_CheekL1', 'FACIAL_L_12IPV_CheekL2', 'FACIAL_L_12IPV_CheekL3',
                  'FACIAL_L_12IPV_CheekL4', 'FACIAL_R_CheekLower1', 'FACIAL_R_CheekLower2', 'FACIAL_R_12IPV_CheekL1',
                  'FACIAL_R_12IPV_CheekL2', 'FACIAL_R_12IPV_CheekL3', 'FACIAL_R_12IPV_CheekL4',
                  'FACIAL_L_NostrilThickness3', 'FACIAL_R_NostrilThickness3', 'FACIAL_C_12IPV_NoseL1',
                  'FACIAL_C_12IPV_NoseL2', 'FACIAL_C_12IPV_NoseTip1', 'FACIAL_C_12IPV_NoseTip2',
                  'FACIAL_C_12IPV_NoseTip3', 'FACIAL_L_12IPV_NoseTip1', 'FACIAL_R_12IPV_NoseTip1',
                  'FACIAL_L_12IPV_NoseTip2', 'FACIAL_R_12IPV_NoseTip2', 'FACIAL_L_12IPV_NoseTip3',
                  'FACIAL_R_12IPV_NoseTip3', 'FACIAL_L_NostrilThickness1', 'FACIAL_L_NostrilThickness2',
                  'FACIAL_L_12IPV_Nostril1', 'FACIAL_L_12IPV_Nostril2', 'FACIAL_L_12IPV_Nostril3',
                  'FACIAL_L_12IPV_Nostril4', 'FACIAL_L_12IPV_Nostril5', 'FACIAL_L_12IPV_Nostril6',
                  'FACIAL_L_12IPV_Nostril7', 'FACIAL_L_12IPV_Nostril8', 'FACIAL_L_12IPV_Nostril9',
                  'FACIAL_L_12IPV_Nostril10', 'FACIAL_L_12IPV_Nostril11', 'FACIAL_L_12IPV_Nostril12',
                  'FACIAL_L_12IPV_Nostril13', 'FACIAL_L_12IPV_Nostril14', 'FACIAL_R_NostrilThickness1',
                  'FACIAL_R_NostrilThickness2', 'FACIAL_R_12IPV_Nostril1', 'FACIAL_R_12IPV_Nostril2',
                  'FACIAL_R_12IPV_Nostril3', 'FACIAL_R_12IPV_Nostril4', 'FACIAL_R_12IPV_Nostril5',
                  'FACIAL_R_12IPV_Nostril6', 'FACIAL_R_12IPV_Nostril7', 'FACIAL_R_12IPV_Nostril8',
                  'FACIAL_R_12IPV_Nostril9', 'FACIAL_R_12IPV_Nostril10', 'FACIAL_R_12IPV_Nostril11',
                  'FACIAL_R_12IPV_Nostril12', 'FACIAL_R_12IPV_Nostril13', 'FACIAL_R_12IPV_Nostril14',
                  'FACIAL_C_LipUpperSkin', 'FACIAL_L_LipUpperSkin', 'FACIAL_R_LipUpperSkin',
                  'FACIAL_L_LipUpperOuterSkin', 'FACIAL_R_LipUpperOuterSkin', 'FACIAL_C_12IPV_LipUpperSkin1',
                  'FACIAL_C_12IPV_LipUpperSkin2', 'FACIAL_L_12IPV_LipUpperSkin', 'FACIAL_R_12IPV_LipUpperSkin',
                  'FACIAL_L_12IPV_LipUpperOuterSkin1', 'FACIAL_R_12IPV_LipUpperOuterSkin1',
                  'FACIAL_L_12IPV_LipUpperOuterSkin2', 'FACIAL_R_12IPV_LipUpperOuterSkin2',
                  'FACIAL_L_12IPV_MouthInteriorUpper1', 'FACIAL_R_12IPV_MouthInteriorUpper1',
                  'FACIAL_L_12IPV_MouthInteriorUpper2', 'FACIAL_R_12IPV_MouthInteriorUpper2', 'FACIAL_C_LipUpper1',
                  'FACIAL_C_LipUpper2', 'FACIAL_C_LipUpper3', 'FACIAL_L_12IPV_LipUpper1', 'FACIAL_R_12IPV_LipUpper1',
                  'FACIAL_L_12IPV_LipUpper2', 'FACIAL_R_12IPV_LipUpper2', 'FACIAL_L_12IPV_LipUpper3',
                  'FACIAL_R_12IPV_LipUpper3', 'FACIAL_L_12IPV_LipUpper4', 'FACIAL_R_12IPV_LipUpper4',
                  'FACIAL_L_12IPV_LipUpper5', 'FACIAL_R_12IPV_LipUpper5', 'FACIAL_L_LipUpper1', 'FACIAL_L_LipUpper2',
                  'FACIAL_L_LipUpper3', 'FACIAL_L_12IPV_LipUpper6', 'FACIAL_L_12IPV_LipUpper7',
                  'FACIAL_L_12IPV_LipUpper8', 'FACIAL_L_12IPV_LipUpper9', 'FACIAL_L_12IPV_LipUpper10',
                  'FACIAL_L_12IPV_LipUpper11', 'FACIAL_L_12IPV_LipUpper12', 'FACIAL_L_12IPV_LipUpper13',
                  'FACIAL_L_12IPV_LipUpper14', 'FACIAL_L_12IPV_LipUpper15', 'FACIAL_R_LipUpper1', 'FACIAL_R_LipUpper2',
                  'FACIAL_R_LipUpper3', 'FACIAL_R_12IPV_LipUpper6', 'FACIAL_R_12IPV_LipUpper7',
                  'FACIAL_R_12IPV_LipUpper8', 'FACIAL_R_12IPV_LipUpper9', 'FACIAL_R_12IPV_LipUpper10',
                  'FACIAL_R_12IPV_LipUpper11', 'FACIAL_R_12IPV_LipUpper12', 'FACIAL_R_12IPV_LipUpper13',
                  'FACIAL_R_12IPV_LipUpper14', 'FACIAL_R_12IPV_LipUpper15', 'FACIAL_L_LipUpperOuter1',
                  'FACIAL_L_LipUpperOuter2', 'FACIAL_L_LipUpperOuter3', 'FACIAL_L_12IPV_LipUpper16',
                  'FACIAL_L_12IPV_LipUpper17', 'FACIAL_L_12IPV_LipUpper18', 'FACIAL_L_12IPV_LipUpper19',
                  'FACIAL_L_12IPV_LipUpper20', 'FACIAL_L_12IPV_LipUpper21', 'FACIAL_L_12IPV_LipUpper22',
                  'FACIAL_L_12IPV_LipUpper23', 'FACIAL_L_12IPV_LipUpper24', 'FACIAL_R_LipUpperOuter1',
                  'FACIAL_R_LipUpperOuter2', 'FACIAL_R_LipUpperOuter3', 'FACIAL_R_12IPV_LipUpper16',
                  'FACIAL_R_12IPV_LipUpper17', 'FACIAL_R_12IPV_LipUpper18', 'FACIAL_R_12IPV_LipUpper19',
                  'FACIAL_R_12IPV_LipUpper20', 'FACIAL_R_12IPV_LipUpper21', 'FACIAL_R_12IPV_LipUpper22',
                  'FACIAL_R_12IPV_LipUpper23', 'FACIAL_R_12IPV_LipUpper24', 'FACIAL_L_LipCorner1',
                  'FACIAL_L_LipCorner2', 'FACIAL_L_LipCorner3', 'FACIAL_L_12IPV_LipCorner1',
                  'FACIAL_L_12IPV_LipCorner2', 'FACIAL_L_12IPV_LipCorner3', 'FACIAL_R_LipCorner1',
                  'FACIAL_R_LipCorner2', 'FACIAL_R_LipCorner3', 'FACIAL_R_12IPV_LipCorner1',
                  'FACIAL_R_12IPV_LipCorner2', 'FACIAL_R_12IPV_LipCorner3', 'FACIAL_L_JawBulge', 'FACIAL_R_JawBulge',
                  'FACIAL_L_JawRecess', 'FACIAL_R_JawRecess', 'FACIAL_L_Masseter', 'FACIAL_R_Masseter',
                  'FACIAL_C_UnderChin', 'FACIAL_L_12IPV_UnderChin1', 'FACIAL_R_12IPV_UnderChin1',
                  'FACIAL_L_12IPV_UnderChin2', 'FACIAL_R_12IPV_UnderChin2', 'FACIAL_L_UnderChin', 'FACIAL_R_UnderChin',
                  'FACIAL_L_12IPV_UnderChin3', 'FACIAL_R_12IPV_UnderChin3', 'FACIAL_L_12IPV_UnderChin4',
                  'FACIAL_R_12IPV_UnderChin4', 'FACIAL_L_12IPV_UnderChin5', 'FACIAL_R_12IPV_UnderChin5',
                  'FACIAL_L_12IPV_UnderChin6', 'FACIAL_R_12IPV_UnderChin6', 'FACIAL_C_LipLowerSkin',
                  'FACIAL_L_LipLowerSkin', 'FACIAL_R_LipLowerSkin', 'FACIAL_L_LipLowerOuterSkin',
                  'FACIAL_R_LipLowerOuterSkin', 'FACIAL_C_12IPV_LipLowerSkin1', 'FACIAL_C_12IPV_LipLowerSkin2',
                  'FACIAL_L_12IPV_LipLowerSkin', 'FACIAL_R_12IPV_LipLowerSkin', 'FACIAL_L_12IPV_LipLowerOuterSkin1',
                  'FACIAL_R_12IPV_LipLowerOuterSkin1', 'FACIAL_L_12IPV_LipLowerOuterSkin2',
                  'FACIAL_R_12IPV_LipLowerOuterSkin2', 'FACIAL_L_12IPV_LipLowerOuterSkin3',
                  'FACIAL_R_12IPV_LipLowerOuterSkin3', 'FACIAL_L_12IPV_MouthInteriorLower1',
                  'FACIAL_R_12IPV_MouthInteriorLower1', 'FACIAL_L_12IPV_MouthInteriorLower2',
                  'FACIAL_R_12IPV_MouthInteriorLower2', 'FACIAL_C_LipLower1', 'FACIAL_C_LipLower2',
                  'FACIAL_C_LipLower3', 'FACIAL_L_12IPV_LipLower1', 'FACIAL_R_12IPV_LipLower1',
                  'FACIAL_L_12IPV_LipLower2', 'FACIAL_R_12IPV_LipLower2', 'FACIAL_L_12IPV_LipLower3',
                  'FACIAL_R_12IPV_LipLower3', 'FACIAL_L_12IPV_LipLower4', 'FACIAL_R_12IPV_LipLower4',
                  'FACIAL_L_12IPV_LipLower5', 'FACIAL_R_12IPV_LipLower5', 'FACIAL_L_LipLower1', 'FACIAL_L_LipLower2',
                  'FACIAL_L_LipLower3', 'FACIAL_L_12IPV_LipLower6', 'FACIAL_L_12IPV_LipLower7',
                  'FACIAL_L_12IPV_LipLower8', 'FACIAL_L_12IPV_LipLower9', 'FACIAL_L_12IPV_LipLower10',
                  'FACIAL_L_12IPV_LipLower11', 'FACIAL_L_12IPV_LipLower12', 'FACIAL_L_12IPV_LipLower13',
                  'FACIAL_L_12IPV_LipLower14', 'FACIAL_L_12IPV_LipLower15', 'FACIAL_R_LipLower1', 'FACIAL_R_LipLower2',
                  'FACIAL_R_LipLower3', 'FACIAL_R_12IPV_LipLower6', 'FACIAL_R_12IPV_LipLower7',
                  'FACIAL_R_12IPV_LipLower8', 'FACIAL_R_12IPV_LipLower9', 'FACIAL_R_12IPV_LipLower10',
                  'FACIAL_R_12IPV_LipLower11', 'FACIAL_R_12IPV_LipLower12', 'FACIAL_R_12IPV_LipLower13',
                  'FACIAL_R_12IPV_LipLower14', 'FACIAL_R_12IPV_LipLower15', 'FACIAL_L_LipLowerOuter1',
                  'FACIAL_L_LipLowerOuter2', 'FACIAL_L_LipLowerOuter3', 'FACIAL_L_12IPV_LipLower16',
                  'FACIAL_L_12IPV_LipLower17', 'FACIAL_L_12IPV_LipLower18', 'FACIAL_L_12IPV_LipLower19',
                  'FACIAL_L_12IPV_LipLower20', 'FACIAL_L_12IPV_LipLower21', 'FACIAL_L_12IPV_LipLower22',
                  'FACIAL_L_12IPV_LipLower23', 'FACIAL_L_12IPV_LipLower24', 'FACIAL_R_LipLowerOuter1',
                  'FACIAL_R_LipLowerOuter2', 'FACIAL_R_LipLowerOuter3', 'FACIAL_R_12IPV_LipLower16',
                  'FACIAL_R_12IPV_LipLower17', 'FACIAL_R_12IPV_LipLower18', 'FACIAL_R_12IPV_LipLower19',
                  'FACIAL_R_12IPV_LipLower20', 'FACIAL_R_12IPV_LipLower21', 'FACIAL_R_12IPV_LipLower22',
                  'FACIAL_R_12IPV_LipLower23', 'FACIAL_R_12IPV_LipLower24', 'FACIAL_C_Jawline',
                  'FACIAL_L_12IPV_Jawline1', 'FACIAL_R_12IPV_Jawline1', 'FACIAL_L_12IPV_Jawline2',
                  'FACIAL_R_12IPV_Jawline2', 'FACIAL_L_Jawline1', 'FACIAL_L_Jawline2', 'FACIAL_L_12IPV_Jawline3',
                  'FACIAL_L_12IPV_Jawline4', 'FACIAL_L_12IPV_Jawline5', 'FACIAL_L_12IPV_Jawline6', 'FACIAL_R_Jawline1',
                  'FACIAL_R_Jawline2', 'FACIAL_R_12IPV_Jawline3', 'FACIAL_R_12IPV_Jawline4', 'FACIAL_R_12IPV_Jawline5',
                  'FACIAL_R_12IPV_Jawline6', 'FACIAL_L_ChinSide', 'FACIAL_R_ChinSide', 'FACIAL_L_12IPV_ChinS1',
                  'FACIAL_R_12IPV_ChinS1', 'FACIAL_L_12IPV_ChinS2', 'FACIAL_R_12IPV_ChinS2', 'FACIAL_L_12IPV_ChinS3',
                  'FACIAL_R_12IPV_ChinS3', 'FACIAL_L_12IPV_ChinS4', 'FACIAL_R_12IPV_ChinS4', 'FACIAL_C_Chin1',
                  'FACIAL_L_Chin1', 'FACIAL_R_Chin1', 'FACIAL_C_Chin2', 'FACIAL_L_Chin2', 'FACIAL_R_Chin2',
                  'FACIAL_C_Chin3', 'FACIAL_L_Chin3', 'FACIAL_R_Chin3', 'FACIAL_L_12IPV_Chin1', 'FACIAL_R_12IPV_Chin1',
                  'FACIAL_L_12IPV_Chin2', 'FACIAL_R_12IPV_Chin2', 'FACIAL_C_12IPV_Chin3', 'FACIAL_C_12IPV_Chin4',
                  'FACIAL_L_12IPV_Chin5', 'FACIAL_R_12IPV_Chin5', 'FACIAL_L_12IPV_Chin6', 'FACIAL_R_12IPV_Chin6',
                  'FACIAL_L_12IPV_Chin7', 'FACIAL_R_12IPV_Chin7', 'FACIAL_L_12IPV_Chin8', 'FACIAL_R_12IPV_Chin8',
                  'FACIAL_L_12IPV_Chin9', 'FACIAL_R_12IPV_Chin9', 'FACIAL_L_12IPV_Chin10', 'FACIAL_R_12IPV_Chin10',
                  'FACIAL_L_12IPV_Chin11', 'FACIAL_R_12IPV_Chin11', 'FACIAL_L_12IPV_Chin12', 'FACIAL_R_12IPV_Chin12',
                  'FACIAL_L_12IPV_Chin13', 'FACIAL_R_12IPV_Chin13', 'FACIAL_L_12IPV_Chin14', 'FACIAL_R_12IPV_Chin14',
                  'FACIAL_C_NoseBridge', 'FACIAL_L_Ear', 'FACIAL_L_Ear1', 'FACIAL_L_Ear2', 'FACIAL_L_Ear3',
                  'FACIAL_L_Ear4', 'FACIAL_R_Ear', 'FACIAL_R_Ear1', 'FACIAL_R_Ear2', 'FACIAL_R_Ear3', 'FACIAL_R_Ear4']

# Adds directories to path
syspath.insert(0, ROOT_DIR)
syspath.insert(0, DATA_DIR)
syspath.insert(0, LIB_DIR)


# Imports
from maya import cmds, mel
import maya.OpenMaya as om
from dna_viewer import (
    DNA,
    Config,
    RigConfig,
    build_meshes,
    build_rig,
    get_skin_weights_from_scene,
    set_skin_weights_to_scene
)
from dnacalib import (
    CommandSequence,
    DNACalibDNAReader,
    RenameJointCommand,
    ScaleCommand,
    SetBlendShapeTargetDeltasCommand,
    SetVertexPositionsCommand,
    CalculateMeshLowerLODsCommand,
    VectorOperation_Add,
    VectorOperation_Interpolate,
    SetNeutralJointTranslationsCommand,
    SetNeutralJointRotationsCommand,
    SetLODsCommand,
    TranslateCommand,
    SetSkinWeightsCommand,
    RemoveJointCommand,
    RotateCommand
)

from dna import (
    BinaryStreamReader,
    BinaryStreamWriter,
    JSONStreamWriter,
    DataLayer_All,
    DataLayer_Behavior,
    FileStream,
    Status,
)
from vtx_color import MESH_SHADER_MAPPING, VTX_COLOR_MESHES, VTX_COLOR_VALUES


# Methods
def read_dna(path):
    stream = FileStream(path, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
    reader = BinaryStreamReader(stream, DataLayer_All)
    reader.read()
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error loading DNA: {status.message}")
    return reader


def save_dna(reader, path):
    stream = FileStream(path, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
    writer = BinaryStreamWriter(stream)
    writer.setFrom(reader)
    writer.write()

    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error saving DNA: {status.message}")

    print(f"DNA {path} successfully saved.")


def show_meshes(dna_path, add_skinning=False, add_blend_shapes=False):
    cmds.file(force=True, new=True)

    dna = DNA(dna_path)

    # Builds and returns the created mesh paths in the scene
    config = Config(
        add_joints=True,
        add_blend_shapes=add_blend_shapes,
        add_skin_cluster=add_skinning,
        add_ctrl_attributes_on_root_joint=True,
        add_animated_map_attributes_on_root_joint=True,
        add_mesh_name_to_blend_shape_channel_name=True,
        add_key_frames=True
    )

    # Build meshes
    build_meshes(dna, config)


def assemble_scene(dna_path, analog_gui_path, gui_path,
                   additional_assemble_script):
    dna = DNA(dna_path)
    config = RigConfig(
        gui_path=gui_path,
        analog_gui_path=analog_gui_path,
        aas_path=additional_assemble_script,
        add_animated_map_attributes_on_root_joint=True,
        add_key_frames=True,
        add_mesh_name_to_blend_shape_channel_name=True
    )

    # Creates the rig
    build_rig(dna=dna, config=config)

    translation = cmds.xform("neck_01", ws=True, query=True, translation=True)
    cmds.xform("CTRL_faceGUI", ws=True, t=[translation[0] + 20, translation[1] + 5, translation[2]])


def get_mesh_vertex_positions_from_scene(meshName):
    try:
        sel = om.MSelectionList()
        sel.add(meshName)

        dag_path = om.MDagPath()
        sel.getDagPath(0, dag_path)

        mf_mesh = om.MFnMesh(dag_path)
        positions = om.MPointArray()

        mf_mesh.getPoints(positions, om.MSpace.kObject)
        return [
            [positions[i].x, positions[i].y, positions[i].z]
            for i in range(positions.length())
        ]
    except RuntimeError:
        print(f"{meshName} is missing, skipping it")
        return None


def run_joints_command(reader, calibrated):
    # Making arrays for joints' transformations and their corresponding mapping arrays
    joint_translations = []
    joint_rotations = []

    for i in range(reader.getJointCount()):
        joint_name = reader.getJointName(i)

        translation = cmds.xform(joint_name, query=True, translation=True)
        joint_translations.append(translation)

        rotation = cmds.joint(joint_name, query=True, orientation=True)
        joint_rotations.append(rotation)

    set_new_joints_translations = SetNeutralJointTranslationsCommand(joint_translations)
    set_new_joints_rotations = SetNeutralJointRotationsCommand(joint_rotations)

    # Abstraction to collect all commands into a sequence, and run them with only one invocation
    commands = CommandSequence()

    commands.add(set_new_joints_translations)
    commands.add(set_new_joints_rotations)

    commands.run(calibrated)
    # verify that everything went fine
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error do_joints_command: {status.message}")


def run_vertices_command(
        calibrated, old_vertices_positions, new_vertices_positions, mesh_index
):
    # making deltas between old vertices positions and new one
    deltas = []
    for new_vertex, old_vertex in zip(new_vertices_positions, old_vertices_positions):
        delta = []
        for new, old in zip(new_vertex, old_vertex):
            delta.append(new - old)
        deltas.append(delta)

    new_neutral_mesh = SetVertexPositionsCommand(
        mesh_index, deltas, VectorOperation_Add
    )

    commands = CommandSequence()

    # Add new vertex position deltas (NOT ABSOLUTE VALUES) onto existing vertex positions
    commands.add(new_neutral_mesh)

    # Recalculate lower LODs based on LOD0
    calculate_command = CalculateMeshLowerLODsCommand()
    commands.add(calculate_command)

    commands.run(calibrated)

    # verify that everything went fine
    if not Status.isOk():
        status = Status.get()
        raise RuntimeError(f"Error do_vertices_command: {status.message}")


def transfer_joints_positions_distance(a, b):
    return pow((a[0] - b[0]), 2) + pow((a[1] - b[1]), 2) + pow((a[2] - b[2]), 2)


def find_and_save_joint_positions_in_file(reader, joints, file_path):
    mesh = reader.getMeshName(0)
    output = {}
    for joint_name in joints:
        cmds.select(joint_name)

        joint_pos = cmds.xform(joint_name, q=True, ws=True, translation=True)
        near_point = mel.eval(f"nearestPointOnMesh {mesh}")
        cmds.setAttr(f"{near_point}.inPositionX", joint_pos[0])
        cmds.setAttr(f"{near_point}.inPositionY", joint_pos[1])
        cmds.setAttr(f"{near_point}.inPositionZ", joint_pos[2])
        best_face = cmds.getAttr(f"{near_point}.nearestFaceIndex")

        face_vtx_str = cmds.polyInfo(f"{mesh}.f[{best_face}]", fv=True)
        buffer = face_vtx_str[0].split()
        closest_vtx = 0
        dist = 10000
        for v in range(2, len(buffer)):
            vtx = buffer[v]
            vtx_pos = cmds.xform(f"{mesh}.vtx[{vtx}]", q=True, ws=True, translation=True)
            new_dist = transfer_joints_positions_distance(joint_pos, vtx_pos)
            if new_dist < dist:
                dist = new_dist
                closest_vtx = vtx
        output[joint_name] = closest_vtx

    with open(file_path, 'w') as out_file:
        json.dump(output, out_file, indent=4)


def prepare_rotated_dna(dna_path, rotated_dna_path):
    reader = read_dna(dna_path)

    # Copies DNA contents and will serve as input/output parameter to commands
    calibrated = DNACalibDNAReader(reader)

    # Modifies calibrated DNA in-place
    rotate = RotateCommand([90.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    rotate.run(calibrated)

    save_dna(calibrated, rotated_dna_path)
    return DNA(rotated_dna_path)


def get_dna(dna_path, rotated_dna_path):
    if up_axis == "z":
        return prepare_rotated_dna(dna_path, rotated_dna_path)
    return DNA(dna_path)


def build_meshes_for_lod(dna, lod):
    # Create config
    config = Config(
        group_by_lod=False,
        create_display_layers=False,
        lod_filter=[lod],
        add_mesh_name_to_blend_shape_channel_name=True,
    )

    # Builds and returns the created mesh paths in the scene
    return build_meshes(dna, config)


def create_skin_cluster(influences, mesh, skin_cluster_name, maximum_influences):
    cmds.select(influences[0], replace=True)
    cmds.select(mesh, add=True)
    skinCluster = cmds.skinCluster(
        toSelectedBones=True,
        name=skin_cluster_name,
        maximumInfluences=maximum_influences,
        skinMethod=0,
        obeyMaxInfluences=True,
    )
    if len(influences) > 1:
        cmds.skinCluster(
            skinCluster, edit=True, addInfluence=influences[1:], weight=0.0
        )
    return skinCluster


def create_head_and_body_scene(mesh_names, body_file, neck_joints, root_joint, facial_root_joints):
    scene_mesh_names = []
    skinweights = []

    for mesh_name in mesh_names:
        if cmds.objExists(mesh_name):
            scene_mesh_names.append(mesh_name)
            skinweights.append(get_skin_weights_from_scene(mesh_name))
            cmds.delete(f"{mesh_name}_skinCluster")

    for facial_joint in facial_root_joints:
        cmds.parent(facial_joint, world=True)
    cmds.delete(root_joint)

    cmds.file(body_file, options="v=0", type="mayaAscii", i=True)
    if up_axis == "y":
        cmds.joint("root", edit=True, orientation=[-90.0, 0.0, 0.0])
    for facial_joint, neck_joint in zip(facial_root_joints, neck_joints):
        cmds.parent(facial_joint, neck_joint)

    for mesh_name, skinweight in zip(scene_mesh_names, skinweights):
        create_skin_cluster(
            skinweight.joints,
            mesh_name,
            f"{mesh_name}_skinCluster",
            skinweight.no_of_influences,
        )
        set_skin_weights_to_scene(mesh_name, skinweight)


def set_fbx_options(orientation):
    # Executes FBX relate commands from the imported plugin
    min_time = cmds.playbackOptions(minTime=True, query=True)
    max_time = cmds.playbackOptions(maxTime=True, query=True)

    cmds.FBXResetExport()
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval(f"FBXExportBakeComplexStart -v {min_time}")
    mel.eval(f"FBXExportBakeComplexEnd -v {max_time}")
    mel.eval("FBXExportConstraints -v true")
    mel.eval("FBXExportSkeletonDefinitions -v true")
    mel.eval("FBXExportInputConnections -v true")
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportCameras -v false")
    mel.eval("FBXExportLights -v false")
    cmds.FBXExportUpAxis(orientation)
    # Deselects objects in Maya
    cmds.select(clear=True)


def create_shader(name):
    cmds.shadingNode("blinn", asShader=True, name=name)

    shading_group = str(
        cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{name}SG",
        )
    )
    cmds.connectAttr(f"{name}.outColor", f"{shading_group}.surfaceShader")
    return shading_group


def add_shader(lod):
    for shader_name, meshes in MESH_SHADER_MAPPING.items():
        shading_group = create_shader(shader_name)
        for mesh in meshes:
            if f"lod{lod}" in mesh:
                try:
                    cmds.select(mesh, replace=True)
                    cmds.sets(edit=True, forceElement=shading_group)
                except Exception as e:
                    print(f"Skipped adding shader for mesh {mesh}. Reason {e}")


def set_vertex_color(lod):
    for m, mesh_name in enumerate(VTX_COLOR_MESHES):
        try:
            if f"lod{lod}" in mesh_name:
                cmds.select(mesh_name)
                for v, rgb in enumerate(VTX_COLOR_VALUES[m]):
                    cmds.polyColorPerVertex(f"{mesh_name}.vtx[{v}]", g=rgb[1], b=rgb[2])
        except Exception as e:
            print(f"Skipped adding vtx color for mesh {mesh_name}. Reason {e}")
            continue


def export_fbx(lod_num, meshes, root_jnt, chr_name, fbx_dir):
    # Selects every mesh in the given lod
    for item in meshes:
        cmds.select(item, add=True)
    # Adds facial root joint to selection
    cmds.select(root_jnt, add=True)
    # Sets the file path
    export_file_name = f"{fbx_dir}/{chr_name}_lod{lod_num}.fbx"
    # Exports the fbx
    mel.eval(f'FBXExport -f "{export_file_name}" -s true')


def export_fbx_for_lod(dna, lod, add_vtx_color, chr_name, body_file, fbx_dir, neck_joints, root_joint, fbx_root_jnt,
                       facial_root_joints, orientation):
    # Creates the meshes for the given lod
    result = build_meshes_for_lod(dna, lod)
    meshes = result.get_all_meshes()
    # Executes FBX relate commands from the imported plugin
    create_head_and_body_scene(meshes, body_file, neck_joints, root_joint, facial_root_joints)
    set_fbx_options(orientation)
    # Saves the result
    if add_vtx_color:
        add_shader(lod)
        set_vertex_color(lod)
    export_fbx(lod, meshes, fbx_root_jnt, chr_name, fbx_dir)


# Setting paths that will be used

# Output folder
output_dir = f"{WORK_DIR}/output"
temp_dir = f"{WORK_DIR}/temp"

# Original MH DNA
character_dna = f"{WORK_DIR}/dna/Lena.dna"

# New neutral head mesh
model = f"{WORK_DIR}/model/Lena_remodel.obj"

# Surface joints
joint_position_file = f"{temp_dir}/joint_position.json"

# In-between DNA paths
mesh_dna = f"{WORK_DIR}/dna/Lena_mesh.dna"
jnt_dna = f"{WORK_DIR}/dna/Lena_jnt.dna"

# Final DNA
final_dna = f"{WORK_DIR}/dna/Lena_final.dna"
rotated_dna = f"{WORK_DIR}/dna/Lena_final.rotated.dna"

# Body file
body_file = f"{WORK_DIR}/model/Lena_skeleton.ma"

# Result scene
review_scene = f"{temp_dir}/review_scene.mb"

# Scene misc files
gui_path = f"{DATA_DIR}/mh4/gui.ma"
analog_gui_path = f"{DATA_DIR}/analog_gui.ma"
aas_path = f"{DATA_DIR}/mh4/additional_assemble_script.py"

# Consts
up_axis = "z"
head_mesh = "head_lod0_mesh"
facial_root_joints = ["FACIAL_C_FacialRoot", "FACIAL_C_Neck1Root", "FACIAL_C_Neck2Root"]
neck_joints = ["head", "neck_01", "neck_02"]
root_joint = "spine_04"
add_vtx_color = True
fbx_root = "root"
character_name = "Lena"

#############################################
# Init work
cmds.loadPlugin("nearestPointOnMesh.mll")

# Create folders
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Steps

# Step 1: Read DNA and build scene
show_meshes(character_dna)
reader = read_dna(character_dna)
calibrated = DNACalibDNAReader(reader)

# Save surface joints positions
find_and_save_joint_positions_in_file(reader, surface_joints, joint_position_file)

# Step 2: Update neutral mesh LOD0 based on provided model

# Add model into scene
cmds.file(model, i=True, mergeNamespacesOnClash=True, namespace=":")

run_vertices_command(
    calibrated, get_mesh_vertex_positions_from_scene(head_mesh),
    get_mesh_vertex_positions_from_scene("Mesh"), 0
)

# Save DNA
save_dna(calibrated, mesh_dna)

# Step 3: Update joints - snap to vertices
show_meshes(mesh_dna)

jnt_data = {}
with open(joint_position_file) as jnt_file:
    jnt_data = json.load(jnt_file)

for jnt_name, vertex_id in jnt_data.items():
    vtx_position = cmds.xform(f"{head_mesh}.vtx[{vertex_id}]", q=True, worldSpace=True, t=True)
    cmds.xform(jnt_name, ws=True, translation=vtx_position)

reader = read_dna(mesh_dna)
calibrated = DNACalibDNAReader(reader)
run_joints_command(reader, calibrated)

# Save DNA
save_dna(calibrated, jnt_dna)

# Step 4: Change anim setup
reader = read_dna(jnt_dna)

stream = FileStream(final_dna, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
writer = BinaryStreamWriter(stream)
writer.setFrom(reader)

new_lods = [2, 3, 4]
anim_lods = reader.getAnimatedMapLODs()
for lod in new_lods:
    writer.setLODAnimatedMapMapping(lod, 0)
    anim_lods[lod] = anim_lods[0]

writer.setAnimatedMapLODs(anim_lods)
writer.write()
if not Status.isOk():
    status = Status.get()
    raise RuntimeError(f"Error saving DNA: {status.message}")

# Step 5: Check result
assemble_scene(final_dna, analog_gui_path, gui_path, aas_path)
cmds.file(rename=review_scene)
cmds.file(save=True)

# Extra: Write DNA file in JSON (without geometry)
# Create DNA reader and writer
stream = FileStream(final_dna, FileStream.AccessMode_Read, FileStream.OpenMode_Binary)
reader = BinaryStreamReader(stream, DataLayer_Behavior)
reader.read()

final_dna_json = final_dna.replace(".dna", ".json")
stream = FileStream(final_dna_json, FileStream.AccessMode_Write, FileStream.OpenMode_Binary)
writer = JSONStreamWriter(stream)
writer.setFrom(reader)

writer.write()
if not Status.isOk():
    status = Status.get()
    raise RuntimeError(f"Error saving DNA: {status.message}")

###################################################################################
# Export FBX
# Loads the builtin plugin needed for FBX
cmds.loadPlugin("fbxmaya.mll")

# Generate workspace.mel
mel.eval(f'setProject "{output_dir}";')

# Export FBX for each lod
cmds.upAxis(ax=up_axis)

dna_for_export = get_dna(final_dna, rotated_dna)
for lod_index in range(dna_for_export.get_lod_count()):
    export_fbx_for_lod(dna_for_export, lod_index, add_vtx_color,
                       character_name, body_file, output_dir, neck_joints,
                       root_joint, fbx_root, facial_root_joints, up_axis)

with contextlib.suppress(FileNotFoundError):
    os.remove(rotated_dna)
