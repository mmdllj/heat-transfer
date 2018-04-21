# -*- coding: utf-8 -*-
# utf-8编码可以使用中文注释
# 以#Gui开头的行表示图形界面操作，不是纯粹的注释行

# Macro Begin: D:\\newFile_freecad.FCMacro +++++++++++++++++++++++++++++++++++++++++++++++++
import FreeCAD
import Part
import PartDesign
import Sketcher
import math
import os


def renewFile():
    workingDirectory = os.path.split(os.path.realpath(__file__))[0]
    file=os.path.join(workingDirectory,"para","out.txt")
    f = open(file, 'w')
    f.write("")
    f.close()


def print_to(outstr):
    workingDirectory = os.path.split(os.path.realpath(__file__))[0]
    file = os.path.join(workingDirectory, "para", "out.txt")
    f = open(file, "a")
    f.write(outstr)
    f.close()

workingDirectory = os.path.split(os.path.realpath(__file__))[0]
renewFile()
# 定义输入参数=============================================input parameters=======================================
modelFolder = os.path.split(os.path.realpath(__file__))[0]
modelFolder = os.path.join(modelFolder, "model")
modelName = "default.iges"  # 输出的文件名
# 长方形通道的宽和长，高度定义为10
W = 120
L = 250
H = 10
# 奇数列球凸半径为Radius1，偶数列球凸半径为Radius2，球心距布置
Radius1 = 8
Radius2 = 10
delta1 = 2
delta2 = 7.5
# d1是奇数列球凸结构的距离，d2是偶数列球凸结构的距离，d3是列与列之列的距离,
# d3应该大于等于PrintR1+PrintR2,PrintR是球凸结构在通道侧壁面的投影半径
d1 = 20
d2 = 15
d3 = 25
# flag标记是不是叉排
isCross = True
# 定义输入参数=============================================input parameters=======================================
# 如果存在model_temp.txt，从文件中读取输入参数+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
tempfile=os.path.join(workingDirectory, "para","model_temp.txt")
if (os.path.exists(tempfile)):
    print_to("reading data from para\model_temp.txt\n")
    f = open(tempfile, "r")
    lines = f.readlines()
    for line in lines:
        print line,  # 后面跟‘，’将忽略换行符
        # print(line,end='')	#python3语法
        strs = line.split(",")
        if ("modelname" in strs[0].lower()):
            modelName = strs[1].strip()
        elif ("modelfolder" in strs[0].lower()):
            modelFolder = strs[1].strip()
        elif ("width" in strs[0].lower()):
            W = float(strs[1].strip())
        elif ("height" in strs[0].lower()):
            H = float(strs[1].strip())
        elif ("length" in strs[0].lower()):
            L = float(strs[1].strip())
        elif ("radius1" in strs[0].lower()):
            Radius1 = float(strs[1].strip())
        elif ("radius2" in strs[0].lower()):
            Radius2 = float(strs[1].strip())
        elif ("delta1" in strs[0].lower()):
            delta1 = float(strs[1].strip())
        elif ("delta2" in strs[0].lower()):
            delta2 = float(strs[1].strip())
        elif ("d1" in strs[0].lower()):
            d1 = float(strs[1].strip())
        elif ("d2" in strs[0].lower()):
            d2 = float(strs[1].strip())
        elif ("d3" in strs[0].lower()):
            d3 = float(strs[1].strip())
        elif ("iscross" in strs[0].lower()):
            if ("false" in strs[1].lower()):
                isCross = False
            else:
                isCross = True
    f.close()
# 如果存在model_temp.txt，从文件中读取输入参数+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print Radius1
print Radius2
print delta1
print delta2
print d1
print d2
print d3
print isCross
# PrintR1和PrintR2为球凸结构在通道侧壁面的投影半径
PrintR1 = math.sqrt(Radius1 * Radius1 - delta1 * delta1)
PrintR2 = math.sqrt(Radius2 * Radius2 - delta2 * delta2)

# 创建的Solid实体保存名称
ZONENAME = "fluid"
# Gui.activateWorkbench("PartDesignWorkbench")
App.newDocument("Unnamed")
# App.setActiveDocument("Unnamed")
# App.ActiveDocument=App.getDocument("Unnamed")
# Gui.ActiveDocument=Gui.getDocument("Unnamed")
# 保存项目为createModel_freecad.FCStd
# App.getDocument("Unnamed").saveAs("C:/Users/YangKe/Documents/createModel_freecad.FCStd")



# 新建草图
App.activeDocument().addObject('Sketcher::SketchObject', 'Sketch')
App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),
                                                      App.Rotation(0.000000, 0.000000, 0.000000, 1.000000))
# Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
# Gui.activeDocument().setEdit('Sketch')
# 新建集几何列表和约束列表geoList、conList
geoList = []
geoList.append(Part.Line(App.Vector(0, 0, 0), App.Vector(L, 0, 0)))
geoList.append(Part.Line(App.Vector(L, 0, 0), App.Vector(L, W, 0)))
geoList.append(Part.Line(App.Vector(L, W, 0), App.Vector(0, W, 0)))
geoList.append(Part.Line(App.Vector(0, W, 0), App.Vector(0, 0, 0)))
App.ActiveDocument.Sketch.addGeometry(geoList, False)
conList = []
conList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
conList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
conList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
conList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
conList.append(Sketcher.Constraint('Horizontal', 0))
conList.append(Sketcher.Constraint('Horizontal', 2))
conList.append(Sketcher.Constraint('Vertical', 1))
conList.append(Sketcher.Constraint('Vertical', 3))
App.ActiveDocument.Sketch.addConstraint(conList)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 1, -1, 1))

App.activeDocument().addObject("PartDesign::Pad", "Pad")
App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
App.activeDocument().Pad.Length = H
App.ActiveDocument.recompute()
# Gui.activeDocument().hide("Sketch")
# Gui.activeDocument().setEdit('Pad',0)
# 当pad type=0的时候，pad.length2是没有效果的
App.ActiveDocument.Pad.Length = H
App.ActiveDocument.Pad.Reversed = 1
App.ActiveDocument.Pad.Midplane = 0
App.ActiveDocument.Pad.Length2 = 0.000000
App.ActiveDocument.Pad.Type = 0
App.ActiveDocument.Pad.UpToFace = None
App.ActiveDocument.recompute()

# 确定所有球窝球心的位置
rows1 = int(W // d1 + 1)
rows2 = int(W // d2 + 1)
columns = int(L // d3)
pad1 = (W % d1) / 2.0
pad2 = (W % d2) / 2.0
pad3 = (L % d3 + d3) / 2.0

print_to("\nrows1=" + str(rows1))
print_to("\nrows2=" + str(rows2))
print_to("\ncolumns=" + str(columns))
print_to("\ninitial pad1=" + str(pad1))
print_to("\ninitial pad2=" + str(pad2))
print_to("\npad3=" + str(pad3))
print_to("\nPrintR1=" + str(PrintR1))
print_to("\nPrintR2=" + str(PrintR2))
if (pad1 < PrintR1):
    # 如果边界间隙小于球凸半径，就少布置一个球凸，增大边界间隙
    rows1 = rows1 - 1
    pad1 = pad1 + d1 / 2.0
if (pad2 < PrintR2):
    rows2 = rows2 - 1
    pad2 = pad2 + d2 / 2.0
if (pad3 <PrintR1):
    columns=columns-1
    pad3=pad3+d3/2.0
if (pad3<PrintR2):
    columns=columns-1
    pad3=pad3+d3/2.0
# 如果是叉排，确保奇偶列球凸结构数量奇偶性不同

if (isCross == True and ((rows1 % 2 == 0 and rows2 % 2 == 0) or (rows1 % 2 == 1 and rows2 % 2 == 1))):
    if (rows1 > rows2):
        rows1 = rows1 - 1
        pad1 = pad1 + d1 / 2.0
    else:
        rows2 = rows2 - 1
        pad2 = pad2 + d2 / 2.0
print_to("\npad1=" + str(pad1))
print_to("\npad2=" + str(pad2))
z1 = delta1  # 球心对应的z坐标
z2 = delta2
sphereNum = 0  # 球的编号
sphereName = ""
for i in range(columns):
    x = pad3 + d3 * i  # 球心对应的x坐标
    if (i % 2 == 0):  # 奇数列，因为i是从0开始的，所以第一列对应的i是0，奇数列对应的索引号是偶数
        for j in range(rows1):
            y = pad1 + d1 * j
            # 球心坐标为(x,y,z)
            sphereName = "Sphere" + str(sphereNum)

            App.ActiveDocument.addObject("Part::Sphere", sphereName)
            App.ActiveDocument.ActiveObject.Label = sphereName
            App.ActiveDocument.recompute()
            App.ActiveDocument.getObject(sphereName).Radius = str(Radius1) + ' mm'
            App.ActiveDocument.getObject(sphereName).Placement = App.Placement(App.Vector(x, y, z1),
                                                                               App.Rotation(App.Vector(0, 0, 1), 0),
                                                                               App.Vector(0, 0, 0))
            sphereNum = sphereNum + 1
    if (i % 2 == 1):  # 偶数列，因为i是从0开始的，所以第二列对应的i是1，偶数列对应的索引号是奇数
        for j in range(rows2):
            y = pad2 + d2 * j

            sphereName = "Sphere" + str(sphereNum)
            App.ActiveDocument.addObject("Part::Sphere", sphereName)
            App.ActiveDocument.ActiveObject.Label = sphereName
            App.ActiveDocument.recompute()
            App.ActiveDocument.getObject(sphereName).Radius = str(Radius2) + ' mm'
            App.ActiveDocument.getObject(sphereName).Placement = App.Placement(App.Vector(x, y, z2),
                                                                               App.Rotation(App.Vector(0, 0, 1), 0),
                                                                               App.Vector(0, 0, 0))
            sphereNum = sphereNum + 1
print_to("\nsphereNum=" + str(sphereNum))
print_to("\nsphereName=" + sphereName)
print_to("\nRadius1=" + str(Radius1))
print_to("\nRadius2=" + str(Radius2))
# 最后需要添加下面这句话，完成模型重建，否则可能出现最后一步操作没有体现到图形界面中
App.ActiveDocument.recompute()

baseName = ZONENAME + "0"
if (sphereNum > 0):  # 如果存在至少一个球体
    # 从pad上cut掉"Sphere0"，第一个球体编号为"Sphere0"
    # Gui.activateWorkbench("PartWorkbench")
    App.activeDocument().addObject("Part::Cut", baseName)
    App.activeDocument().getObject(baseName).Base = App.activeDocument().getObject("Pad")
    App.activeDocument().getObject(baseName).Tool = App.activeDocument().getObject("Sphere0")
    # Gui.activeDocument().hide("Pad")
    # Gui.activeDocument().hide("Sphere0")
    # Gui.ActiveDocument.getObject(baseName).ShapeColor=Gui.ActiveDocument.getObject("Pad").ShapeColor
    # Gui.ActiveDocument.getObject(baseName).DisplayMode=Gui.ActiveDocument.getObject("Pad").DisplayMode
    App.ActiveDocument.recompute()
if (sphereNum > 1):  # 如果存在多于两个球体
    for i in range(sphereNum - 1):
        baseName = ZONENAME + str(i)
        sphereName = "Sphere" + str(i + 1)  # 第二个球体的名字，第n个球体的名字为"Sphere"+str(n-1)
        cutName = ZONENAME + str(i + 1)  # “fluid”后面的数字n表示减去了n+1个球之后的结构名

        App.activeDocument().addObject("Part::Cut", cutName)
        App.activeDocument().getObject(cutName).Base = App.activeDocument().getObject(baseName)
        App.activeDocument().getObject(cutName).Tool = App.activeDocument().getObject(sphereName)
        # Gui.activeDocument().hide(baseName)
        # Gui.activeDocument().hide(sphereName)
        # Gui.ActiveDocument.getObject(cutName).ShapeColor=Gui.ActiveDocument.getObject(baseName).ShapeColor
        # Gui.ActiveDocument.getObject(cutName).DisplayMode=Gui.ActiveDocument.getObject(baseName).DisplayMode
        App.ActiveDocument.recompute()

__objs__ = []
object=ZONENAME + str(sphereNum - 1)
print_to("\nZoneName=" + object)
__objs__.append(FreeCAD.ActiveDocument.getObject(object))
print_to("\nmodelFile="+os.path.join(modelFolder, modelName))
Part.export(__objs__, (os.path.join(modelFolder, modelName)))

del __objs__
# exit()
