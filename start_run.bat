@echo off 
echo ����Solidworks��ICEM��Fluent·��
echo Ĭ��ʹ��ϵͳ����������ICEMCFD_ROOT150��ֵ��Ϊ���񻮷����·��

echo ��鲢�����ļ���
if exist "%~dp0model" (
echo model�ļ��д��ڣ���������
) else (
echo ����model�ļ���
md "%~dp0model"
)
if exist "%~dp0mesh" (
echo mesh�ļ��д��ڣ���������
) else (
echo ����mesh�ļ���
md "%~dp0mesh"
)
if exist "%~dp0solve" (
echo solve�ļ��д��ڣ���������
) else (
echo ����solve�ļ���
md "%~dp0solve"
)
if exist "%~dp0result" (
echo result�ļ��д��ڣ���������
) else (
echo ����result�ļ���
md "%~dp0result"
)

call python %~dp0createModelFromGivenFile.py
rem �ô�����pythonֻ��ʹ��call������ʹ��start,ʹ��start�ᵼ���������ȴ�python������Ͼ�ִ���������
call python %~dp0createMesh.py
call python %~dp0createSolve.py default
call python %~dp0dataProcess.py default


