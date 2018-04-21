# encoding=UTF8
#  python2
import os
import shutil

def recursionReplace(file, src, sphereNum):#src是需要替换的标记字符串，sphereNum决定了替换的结果又多少个行
    #逐行读取源文件内容，替换需要替换的行，将结果写入临时文件
    file1 = open(file, "r")
    file2 = open("tempFile.txt", "w")
    replaceLine = ""
    for line in file1:
        if (src) in line:
            for num in range(7, sphereNum + 7):
                replaceLine = replaceLine + line.replace(src, "PART_" + str(num)) + "\n"
            line = replaceLine
        file2.write(line)
    file1.close()
    file2.close()
    #删除源文件，将临时文件内容写入源文件名
    os.remove(file)
    file1=open(file,"w")
    file2=open("tempFile.txt","r")
    for line in file2:
        file1.write(line)
    file1.close()
    file2.close()
    os.remove("tempFile.txt")#删除临时文件

def getPartListAndModelFile(file):
    sphereNum = 0

    partListExcept_SixSurface = ""
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
        partListExcept_SixSurface=partListExcept_SixSurface+"PART_"+str(i+7)+" "
        familyPartNumExcept_SixSurface=familyPartNumExcept_SixSurface+"family PART_"+str(i+7)+" "
        part_PART_NUM2ExceptSixSurface=part_PART_NUM2ExceptSixSurface+"part-PART_"+str(i+7)+" 2 "
    CREATED_MATERIAL_NUM="CREATED_MATERIAL_"+str(sphereNum+6+1)
    return partListExcept_SixSurface,familyPartNumExcept_SixSurface,part_PART_NUM2ExceptSixSurface,sphereNum,modelFile


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


workingDirectory = os.path.split(os.path.realpath(__file__))[0]  # 该文件所在的目录，不是本文件的路径名，而是包含它的目录路径
modelFolder = os.path.join(workingDirectory, "model")
paraFolder = os.path.join(workingDirectory, "para")
meshFolder = os.path.join(workingDirectory, "mesh")
outFile = os.path.join(paraFolder, "out.txt")
model_temp = os.path.join(paraFolder, "model_temp.txt")
# 判断网格是否存在
isExist = False
modelName = ""
meshFile = ""
with open(model_temp) as f:
    for line in f:
        if "isExist" in line:
            isExist = line.split(",")[1]
        if "modelName" in line:
            modelName = line.split(",")[1]
            modelName, ext = os.path.splitext(modelName)
if (isExist == True):
    meshFile = modelName + ".msh"
else:
    # 网格文件名为meshName="mesh"+str(modelNumber)
    print("debug: 划分网格...")
    partListExcept_SixSurface,familyPartNumExcept_SixSurface,part_PART_NUM2ExceptSixSurface, sphereNum,modelFile = getPartListAndModelFile(outFile)
    modelFolder, modelFile_relative = os.path.split(modelFile)
    modelName, ext = os.path.splitext(modelFile_relative)
    # 复制"para\case.rpl"到"mesh\modelName.rpl"
    srcfile = os.path.join(paraFolder, "case.rpl")
    dstfile = os.path.join(meshFolder, modelName + ".rpl")
    shutil.copyfile(srcfile, dstfile)
    # 获得网格中所有part的名称列表字符串用于替换网格宏文件相应内容

    created_material_num="CREATED_MATERIAL_"+str(sphereNum+7)
    replaceStringInFile(dstfile, "$wdir$", meshFolder.replace("\\", "/"))
    replaceStringInFile(dstfile, "$modelFolder$", modelFolder.replace("\\", "/"))
    replaceStringInFile(dstfile, "$pureModel$", modelName)
    replaceStringInFile(dstfile, "$family PART_NUMExcept_SixSurface$",familyPartNumExcept_SixSurface)
    replaceStringInFile(dstfile, "$partListExcept_SixSurface$",partListExcept_SixSurface)
    replaceStringInFile(dstfile, "$part-PART_NUM 2_ExceptSixSurface$",part_PART_NUM2ExceptSixSurface)
    replaceStringInFile(dstfile, "$CREATED_MATERIAL_NUM$",created_material_num)
    recursionReplace(dstfile, "$recursion_PartListExcept_SixSurface$", sphereNum)
    # 调用ICEM
    env_dist = os.environ
    icem = env_dist.get('ICEMCFD_ROOT150')

    icem = os.path.join(icem, "win64_amd", "bin", "icemcfd.bat")
    icemcommand = icem + " -batch -script " + dstfile
    # os.popen(icemcommand)
    import subprocess

    subprocess.call([icem, "-batch", "-script", dstfile], shell=True)
    # "%ICEMCFD_ROOT150%\win64_amd\bin\icemcfd.bat" - batch - script % ~dp0mesh\ % core %.rpl
    # 计算
