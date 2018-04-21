@echo off 
echo 设置Solidworks、ICEM、Fluent路径
echo 默认使用系统环境变量中ICEMCFD_ROOT150的值作为网格划分软件路径

echo 检查并创建文件夹
if exist "%~dp0model" (
echo model文件夹存在，不做处理
) else (
echo 创建model文件夹
md "%~dp0model"
)
if exist "%~dp0mesh" (
echo mesh文件夹存在，不做处理
) else (
echo 创建mesh文件夹
md "%~dp0mesh"
)
if exist "%~dp0solve" (
echo solve文件夹存在，不做处理
) else (
echo 创建solve文件夹
md "%~dp0solve"
)
if exist "%~dp0result" (
echo result文件夹存在，不做处理
) else (
echo 创建result文件夹
md "%~dp0result"
)

call python %~dp0createModelFromGivenFile.py
rem 该处调用python只能使用call，不能使用start,使用start会导致批处理不等待python调用完毕就执行以下语句
call python %~dp0createMesh.py
call python %~dp0createSolve.py default
call python %~dp0dataProcess.py default


