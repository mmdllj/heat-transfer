# encoding=UTF8
#  python2

import math
import random
import os
import sys
import shutil  # 用于复制文件


def createRandomParameters():
    print("create random parameters...")
    r1 = random.uniform(1, 20)
    r2 = random.uniform(1, 20)
    if (r1 < 8):
        delta1 = random.uniform(-r1 + 0.1, r1)  # delta1可以取值[x,y)，delta1的值不能取到-r1,所以加一个小值进行限制
    else:
        delta1 = random.uniform(-8 + 0.1, r1)
    if (r2 < 8):
        delta2 = random.uniform(-r2 + 0.1, r2)
    else:
        delta2 = random.uniform(-8 + 0.1, r2)
    pr1 = math.sqrt(r1 * r1 - delta1 * delta1)
    pr2 = math.sqrt(r2 * r2 - delta2 * delta2)
    if (delta1<0):#如果delta为负值，那么那个球凸之间的距离应该判断球凸半径r的大小，所以把投影半径改为r
        pr1=r1
    if (delta2<0):
        pr2=r2
    d1 = random.uniform(2 * pr1 + 0.1, 40)  # delta为正值时，取到下限也没关系，delta为负值时，不能取到下限
    d2 = random.uniform(2 * pr2 + 0.1, 40)
    d3 = random.uniform(pr1 + pr2, 40)
    isCross = str(random.randint(0, 1))
    if (isCross == "0"):
        isCross = "False"
    else:
        isCross = "True"
    if (r1 - delta1 > 9):
        r1, r2, delta1, delta2, d1, d2, d3, isCross = createRandomParameters()
    elif (r2 - delta2 > 9):
        r1, r2, delta1, delta2, d1, d2, d3, isCross = createRandomParameters()
    return r1, r2, delta1, delta2, d1, d2, d3, isCross

def readParaFromFile(file):
    fo=open(file, "r")
    dataLine=fo.read()
    data=dataLine.split(',')
    r1=float(data[0])
    r2=float(data[1])
    delta1=float(data[2])
    delta2=float(data[3])
    d1=float(data[4])
    d2=float(data[5])
    d3=float(data[6])
    isCrossNum=float(data[7])
    isCross=False
    if isCrossNum<0.5:
        isCross=False
    else:
        isCross=True

    fo.close()
    return r1, r2, delta1, delta2, d1, d2, d3, isCross


def writeModelPara(modelFolder, modelRespo, path, r1, r2, delta1, delta2, d1, d2, d3, isCross):  # 返回当前模型对应的编号，和是否存在
    # 将当前模型参数写入模型参数统计文件===============================================================================
    number = -1
    if (os.path.exists(modelRespo)):
        modelNumber = isExists(modelRespo, r1, r2, delta1, delta2, d1, d2, d3, isCross)
        if (modelNumber != -1):  # 如果模型存在，更改临时文件，主要更改modelName
            fo = open(path, "w")
            fo.write("Radius1," + str(r1) + "\n")
            fo.write("Radius2," + str(r2) + "\n")
            fo.write("delta1," + str(delta1) + "\n")
            fo.write("delta2," + str(delta2) + "\n")
            fo.write("d1," + str(d1) + "\n")
            fo.write("d2," + str(d2) + "\n")
            fo.write("d3," + str(d3) + "\n")
            fo.write("isCross," + str(isCross) + "\n")
            fo.write("modelFolder," + modelFolder + "\n")
            fo.write("modelName," + "model" + str(modelNumber) + ".iges\n")
            fo.write("isExist,True")
            fo.close()
            return modelNumber, True
        print("model not exists...........................")
        fp = open(modelRespo, "r")
        line = fp.readline()
        #读取“model.txt”，获得当前模型的编号
        while line:
            # print line
            if len(line.strip()) != 0:  # 不是空行
                if not (line.startswith("ModelNumber")):
                    if (int(line.split(",")[0]) > number):
                        number = int(line.split(",")[0])
            line = fp.readline()
        fp.close()
        #根据当前模型编号和模型参数更新“model.txt”文件
        fp = open(modelRespo, "a")
        number = number + 1
        fp.write("\r\n" + str(number) + "," + str(r1) + "," + str(r2) + "," + str(delta1) + ","
                 + str(delta2) + "," + str(d1) + "," + str(d2) + "," + str(d3) + "," + str(isCross))
        fp.close()
    else:
        print("创建模型参数列表文件...".decode('utf8'))
        fp = open(modelRespo, "w")
        fp.write("ModelNumber, Radius1, Radius2, delta1, delta2, d1, d2, d3, isCross\r\n")
        fp.write("0," + str(r1) + "," + str(r2) + "," + str(delta1) + "," + str(delta2) + "," + str(d1) + "," + str(
            d2) + "," + str(d3) + "," + str(isCross))
        fp.close()
        number = 0
    # 将当前模型参数写入模型参数文件===========================================================================
    print("write result to file...")  # 写出临时文件，用于当前建模
    fo = open(path, "w")
    fo.write("Radius1," + str(r1) + "\n")
    fo.write("Radius2," + str(r2) + "\n")
    fo.write("delta1," + str(delta1) + "\n")
    fo.write("delta2," + str(delta2) + "\n")
    fo.write("d1," + str(d1) + "\n")
    fo.write("d2," + str(d2) + "\n")
    fo.write("d3," + str(d3) + "\n")
    fo.write("isCross," + str(isCross) + "\n")
    fo.write("modelFolder," + modelFolder + "\n")
    fo.write("modelName," + "model" + str(number) + ".iges\n")
    fo.write("isExist,False")
    fo.close()
    return number, False


def isExists(modelRespo, current_r1, current_r2, current_delta1, current_delta2, current_d1, current_d2, current_d3,
             current_isCross):  # 如果存在，返回模型编号，不存在，返回-1
    fp = open(modelRespo, "r")
    line = fp.readline()
    while line:
        # print line
        if len(line.strip()):
            if not line.startswith("ModelNumber"):
                current_r1 = float(line.split(",")[1])
                current_r2 = float(line.split(",")[2])
                current_delta1 = float(line.split(",")[3])
                current_delta2 = float(line.split(",")[4])
                current_d1 = float(line.split(",")[5])
                current_d2 = float(line.split(",")[6])
                current_d3 = float(line.split(",")[7])
                current_isCross = str(line.split(",")[8])
                if (abs(current_r1 - r1) < 0.2) and (abs(current_r2 - r2) < 0.2) and (
                            abs(current_delta1 - delta1) < 0.2) and (abs(current_delta2 - delta2) < 0.2) and (
                            abs(current_d1 - d1) < 0.2) and (abs(current_d2 - d2) < 0.2) and (
                            abs(current_d3 - d3) < 0.2) and (
                            current_isCross == isCross):
                    return line.split(",")[0]
        line = fp.readline()
    fp.close()
    return -1


def getPartList(file):
    sphereNum = 0
    meshPartList = ""
    with open(file) as f:
        for line in f:
            if "sphereNum" in line:
                sphereNum = int(line.split("=")[1])
    for i in range(sphereNum):
        meshPartList = meshPartList + "PART_" + str(i + 1) + " "
    return meshPartList


def replaceStringInFile(file, oldStr, newStr):
    t = ""
    with open(file, 'r+') as f:
        t = f.read()
        t = t.replace(oldStr, newStr)
        # f=seek(0,0)    网上给的这两行代码会出错，出错内容：最后两行代码会部分截断重复（倒数第二行一部分和倒数第一行重复），怀疑可能原因与python字符串缓存输出流有关
        # f.write(t)
        f.close()
    fw = open(file, "w")
    fw.write(t)
    fw.close()


if __name__ == '__main__':  # java调用时传入(workingDirectory, modelFolder, meshFolder,
    inputParaNumbers = len(sys.argv)
    workingDirectory = os.path.split(os.path.realpath(__file__))[0]  # 该文件所在的目录，不是本文件的路径名，而是包含它的目录路径
    modelFolder = os.path.join(workingDirectory, "model")
    paraFolder = os.path.join(workingDirectory, "para")
    meshFolder = os.path.join(workingDirectory, "mesh")
    outFile = os.path.join(paraFolder, "out.txt")
    if (inputParaNumbers > 1):
        workingDirectory = sys.argv[1]
        modelFolder = sys.argv[2]
        meshFolder = sys.argv[3]
    print ("debug:" + workingDirectory)
    print ("debug:" + modelFolder)

    r1, r2, delta1, delta2, d1, d2, d3, isCross = readParaFromFile(os.path.join(paraFolder, "givenByMATLAB.txt"))

    # 查看满足当前模型参数的模型是否存在
    modelRespo = os.path.join(paraFolder, "model.txt")
    print("debug:" + modelRespo)
    modelNumber, isExist = writeModelPara(modelFolder, modelRespo, os.path.join(paraFolder, "model_temp.txt"), r1, r2,
                                          delta1, delta2, d1,
                                          d2, d3, isCross)  # 当前模型参数在modelRespo中所对应的编号
    modelName = "model" + str(modelNumber)
    if (isExist):  # 如果模型已经存在，取得网格文件
        # 网格文件名为meshName="mesh"+str(modelNumber)
        print("debug: 使用已经存在的网格文件" + modelName)
    else:  # 如果不存在，创建模型，划分网格
        os.system("python " + os.path.join(workingDirectory, "createModel_freecad.py"))
