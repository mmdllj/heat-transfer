# encoding=UTF8
#  python2
import os
import sys

def readDataFromFile(file):
    flowrate = 0.0
    pressure_inlet = 0.0
    pressure_outlet = 0.0
    temperature_wall = 0.0
    temperature_fluid = 0.0
    with open(file) as f:
        for line in f:
            if ("flowrate") in line:
                tempStr = line.split(":")[1].strip()
                tempStr = tempStr.split(" ")[0]
                flowrate = float(tempStr)
            elif ("wall temperature") in line:
                tempStr = line.split(":")[1].strip()
                tempStr = tempStr.split(" ")[0]
                temperature_wall = float(tempStr)
            elif ("fluid temperature") in line:
                tempStr = line.split(":")[1].strip()
                tempStr = tempStr.split(" ")[0]
                temperature_fluid = float(tempStr)
            elif ("inlet pressure") in line:
                tempStr = line.split(":")[1].strip()
                tempStr = tempStr.split(" ")[0]
                pressure_inlet = float(tempStr)
            elif ("outlet pressure") in line:
                tempStr = line.split(":")[1].strip()
                tempStr = tempStr.split(" ")[0]
                pressure_outlet = float(tempStr)
    return pressure_inlet, pressure_outlet, temperature_wall, temperature_fluid, flowrate


def readInputParaFromFile(file):
    r1 = 0.0
    r2 = 0.0
    delta1 = 0.0
    delta2 = 0.0
    d1 = 0.0
    d2 = 0.0
    d3 = 0.0
    isCross = False
    modelName = ""
    with open(file) as f:
        for line in f:
            if ("Radius1") in line:
                r1 = float(line.split(",")[1])
            elif ("Radius2") in line:
                r2 = float(line.split(",")[1])
            elif ("delta1") in line:
                delta1 = float(line.split(",")[1])
            elif ("delta2") in line:
                delta2 = float(line.split(",")[1])
            elif ("d1") in line:
                d1 = float(line.split(",")[1])
            elif ("d2") in line:
                d2 = float(line.split(",")[1])
            elif ("d3") in line:
                d3 = float(line.split(",")[1])
            elif ("isCross") in line:
                tempStr = line.split(",")[1]
                if (tempStr.strip() == "False"):
                    isCross = False
                else:
                    isCross = True
            elif ("modelName") in line:
                modelName = line.split(",")[1]
                modelName, ext = os.path.splitext(modelName)
    return modelName, r1, r2, delta1, delta2, d1, d2, d3, isCross


def readBoundaryConditions(file):
    heatflux = 0.0
    velocity = 0.0
    with open(file) as f:
        for line in f:
            if (line.startswith("boundaryConditionsName")):
                continue
            elif (line.strip()):  # 如果line不是空行
                list = line.split(",")
                heatflux = float(list[1])
                velocity = float(list[2])
    return heatflux, velocity


if __name__ == '__main__':
    workingDirectory = os.path.split(os.path.realpath(__file__))[0]  # 该文件所在的目录，不是本文件的路径名，而是包含它的目录路径
    modelFolder = os.path.join(workingDirectory, "model")
    paraFolder = os.path.join(workingDirectory, "para")
    resultFolder = os.path.join(workingDirectory, "result")
    solveFolder = os.path.join(workingDirectory, "solve")
    outFile = os.path.join(paraFolder, "out.txt")
    model_temp = os.path.join(paraFolder, "model_temp.txt")
    bcfile = os.path.join(workingDirectory, "boundaryConditions.csv")
    resultFile = os.path.join(resultFolder, "result.txt")

    pureCaseName = ""
    command = sys.argv[1];

    if command == "default":    #获得pureCaseName
        print("debug: dataProcess " + command)
        # 获得pureCaseName
        # 获得模型编号
        import createSolve
        modelName = createSolve.getModelName(model_temp)
        # 读取材料参数
        materialName = createSolve.readMaterial(os.path.join(workingDirectory, "materials.csv"))
        # 读取边界条件参数
        boundaryCondition = createSolve.readBoundaryCondition(os.path.join(workingDirectory, "boundaryConditions.csv"))
        pureCaseName = modelName + "_" + materialName + "_" + boundaryCondition
    elif command == "pureCaseName": #由调用该脚本的java程序传入pureCaseName
        pureCaseName = sys.argv[2]

    # 读取计算结果
    tableFile = os.path.join(solveFolder, pureCaseName, pureCaseName + ".txt")
    pressure_inlet, pressure_outlet, temperature_wall, temperature_fluid, flowrate = readDataFromFile(tableFile)
    # 读取计算使用的输入参数，本例中只有模型参数变化
    modelName, r1, r2, delta1, delta2, d1, d2, d3, isCross = readInputParaFromFile(model_temp)
    # 读取边界条件参数
    heatflux, velocity = readBoundaryConditions(bcfile)
    width = 0.12  # 通道截面宽度
    height = 0.01  # 通道界面高度
    length = 0.25  # 通道长度
    d_h = 2 * width * height / (width + height)  # 水利直径
    namuda = 0.592
    rou = 998.7
    deltaT = temperature_wall - temperature_fluid  # 流体温度和壁面温度的温度差
    deltaP = pressure_inlet - pressure_outlet  # 进出口压力差
    h = heatflux / deltaT  # 对流换热系数
    nu = h * d_h / namuda  # 努赛尔数
    friction = deltaP / length * d_h / (2 * rou * velocity * velocity)
    tp = nu * friction ** (-1 / 3)
    rela_nu = "rela_nu"
    rela_f = "rela_f"
    rela_tp = "rela_tp"
    # 将数据写入result.txt文件
    if (os.path.exists(resultFile)):
        with open(resultFile, "a") as f:
            f.write(
                modelName + "," + str(r1) + "," + str(r2) + "," + str(delta1) + "," + str(delta2) + "," + str(d1) + "," \
                + str(d2) + "," + str(d3) + "," + str(isCross) + "," + str(flowrate) + "," + str(pressure_inlet) + "," \
                + str(pressure_outlet) + "," + str(temperature_wall) + "," + str(temperature_fluid) + "," + str(nu) \
                + "," + str(friction) + "," + str(tp) + "," + str(rela_nu) + "," + str(rela_f) + "," + str(
                    rela_tp) + "\n")
    else:
        with open(resultFile, "w") as f:
            f.write("modelName,\tradius1,\tradius2,\tdelta1,\tdelta2,\td1,\td2,\td3,\tisCross,\t\
                    flowrate,\tP_in,\tP_out,\tT_wall,\tT_fluid,\tNu,\tfriction,\ttp,\trela_Nu,\
                    \trela_f,\trela_tp\n")
            f.write(
                modelName + "," + str(r1) + "," + str(r2) + "," + str(delta1) + "," + str(delta2) + "," + str(d1) + "," \
                + str(d2) + "," + str(d3) + "," + str(isCross) + "," + str(flowrate) + "," + str(pressure_inlet) + "," \
                + str(pressure_outlet) + "," + str(temperature_wall) + "," + str(temperature_fluid) + "," + str(nu) \
                + "," + str(friction) + "," + str(tp) + "," + str(rela_nu) + "," + str(rela_f) + "," + str(
                    rela_tp) + "\n")

    if command=="default":#还需要更新数据库文件
        pass