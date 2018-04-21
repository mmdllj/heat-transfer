# encoding=UTF8
#  python2
import os
import shutil
import sys

# 替换$solveFolder$/$pureCaseName$/$pureCaseName$ solveFolder的路径分隔符为/
# 替换$meshFile$ meshFile的路径分隔符为\

def getPartListAndModelFile(file):
    sphereNum = 0
    meshPartList = ""
    partListExcept_SixSurface_comma = ""
    familyPartNumExcept_SixSurface = ""
    part_PART_NUM2ExceptSixSurface = ""
    modelFile = ""
    with open(file) as f:
        for line in f:
            if "sphereNum" in line:
                sphereNum = int(line.split("=")[1])
            elif "modelFile" in line:
                modelFile = line.split("=")[1]
    for i in range(sphereNum):
        meshPartList = meshPartList + "PART_" + str(i + 1) + " "
        partListExcept_SixSurface_comma=partListExcept_SixSurface_comma+"PART_"+str(i+7)+","

    partListExcept_SixSurface_comma=partListExcept_SixSurface_comma[0:-1]
    CREATED_MATERIAL_NUM="CREATED_MATERIAL_"+str(sphereNum+6+1)
    return meshPartList,partListExcept_SixSurface_comma,sphereNum,modelFile



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

def getModelName(file):
    with open(file, "r+") as f:
        for line in f:
            if "isExist" in line:
                isExist = line.split(",")[1]
            if "modelName" in line:
                modelName = line.split(",")[1].strip()
                modelName, ext = os.path.splitext(modelName)
    return modelName

def readMaterial(file):
    return "water"

def readBoundaryCondition(file):
    return "1"
if __name__ == '__main__':
    # 传入参数，命令+pureCaseName
    # 命令为default时，完全由该脚本完成计算，只能针对单一边界条件和流动工质
    # 命令为pureCaseName时，由java完成部分工作，该脚本值修改pureCaseName对应的文件的部分变量
    workingDirectory = os.path.split(os.path.realpath(__file__))[0]  # 该文件所在的目录，不是本文件的路径名，而是包含它的目录路径
    modelFolder = os.path.join(workingDirectory, "model")
    paraFolder = os.path.join(workingDirectory, "para")
    meshFolder = os.path.join(workingDirectory, "mesh")
    solveFolder=os.path.join(workingDirectory, "solve")
    outFile = os.path.join(paraFolder, "out.txt")
    model_temp = os.path.join(paraFolder, "model_temp.txt")
    pureCaseName=""
    command = sys.argv[1];

    if command == "default":
        print("debug: createSolve " + command)
        # 获得pureCaseName
        # 获得模型编号
        modelName=getModelName(model_temp)
        # 读取材料参数
        materialName=readMaterial(os.path.join(workingDirectory, "materials.csv"))
        # 读取边界条件参数
        boundaryCondition=readBoundaryCondition(os.path.join(workingDirectory, "boundaryConditions.csv"))
        pureCaseName=modelName+"_"+materialName+"_"+boundaryCondition
        # 复制"para\createSolve.wbjn"到"solve\createSolve.wbjn"
        srcfile = os.path.join(paraFolder, "createSolve.wbjn")
        dstfile = os.path.join(solveFolder, pureCaseName + ".wbjn")
        shutil.copyfile(srcfile, dstfile)
    elif command=="pureCaseName":
        print("debug: createSolve " + command + " " + sys.argv[2])
        pureCaseName=sys.argv[2]
        modelName=getModelName(model_temp)
        # 复制"para\createSolve.wbjn"到"solve\modelName.wbjn"，该操作有java主程序完成了，这里直接修改tempSolveFile.jou文件就好
        dstfile = os.path.join(solveFolder, "tempSolveFile.jou")#此时，临时文件还没有被重命名为pureCaseName.wbjn

    meshPartList,partListExcept_SixSurface_Comma, sphereNum,modelFile = getPartListAndModelFile(outFile)
    meshFile=os.path.join(meshFolder, modelName+".msh")

    created_material_num="CREATED_MATERIAL_"+str(sphereNum+7)
    replaceStringInFile(dstfile, "$solveFolder/$", solveFolder.replace("\\","/"))
    replaceStringInFile(dstfile, "$solveFolder$", solveFolder)
    replaceStringInFile(dstfile, "$meshFile$", meshFile)
    replaceStringInFile(dstfile, "$flowrate$", "0.042")
    replaceStringInFile(dstfile, "$partListExcept_SixSurface_Comma$", partListExcept_SixSurface_Comma)
    replaceStringInFile(dstfile, "$pureCaseName$", pureCaseName)
    replaceStringInFile(dstfile, "$CREATED_MATERIAL_NUM$", created_material_num)

    if command=="default":
        #调用CFX开始计算
        # 调用ICEM
        env_dist = os.environ
        ansys = env_dist.get('AWP_ROOT150')

        workBench = os.path.join(ansys, "Framework", "bin","Win64", "runwb2")

        # os.popen(icemcommand)
        import subprocess
        print("solving......")
        subprocess.call([workBench, "-I", "-B","-R", dstfile], shell=True)
        print("...solution done!...")