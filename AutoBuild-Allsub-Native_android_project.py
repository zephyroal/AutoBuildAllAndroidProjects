#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于批量编译NativeAndroid程序
#AutoBuild all sub native android projects
#Zephyr 20141203 Innovation 
import os
import sys

#指定编译目录名
targetBuildDir = 'jni' #'Android'
#指定目标Android版本
targetVersion = 'android-18'
#Build Configuration调试模式 debug/release
Configuration= 'debug'
#是否输出详细编译信息
VerbosBuildInfo = 1
#黑名单，如果遇到以下目录，就不再予以遍历
blackList = ['obj','res','libs','bin','iOS','src']

#全局变量
curRootDir = os.getcwd()
dirVec=[]

def GetProcessorCount():
    try:
        platform = sys.platform
        if platform == 'win32':
            if 'NUMBER_OF_PROCESSORS' in os.environ:
                return int(os.environ['NUMBER_OF_PROCESSORS'])
            else:
                return 8
        else:
            from numpy.distutils import cpuinfo
            return cpuinfo.cpu._getNCPUs()
    except Exception:
        print('Cannot know cpuinfo, use default 4 cpu')
        return 8

def WalkDir(rootDir, level=1): 
	if level==1: print rootDir 
	for lists in os.listdir(rootDir): 
		path = os.path.join(rootDir, lists) 
		if os.path.isdir(path): 
			print '│  '*(level-1)+'│--'+lists 
			if not lists in blackList:
				if lists == targetBuildDir:
					#print('-----path: '+path) 
					#取得父级目录
					parentDir = os.path.dirname(path) 
					#print('-----parentDir: '+parentDir) 
					dirVec.append(parentDir)
					print('-----添加编译目录：'+parentDir) 
				else:
					WalkDir(path, level+1) 

def DoBuild():
	print('---------开始DoBuild---------')
	numProcessor = GetProcessorCount()
	UpdateCMD = 'android update project  -p . -s -t %s' % (targetVersion)
	print('UpdateCMD: '+UpdateCMD)
	isDebug = ( Configuration == 'debug' )
	NDKBuildCMD = 'ndk-build V=%d -j%d NDK_DEBUG=%d' % (VerbosBuildInfo, numProcessor, isDebug)
	print('NDKBuildCMD: '+NDKBuildCMD)
	AntCMD = 'ant %s install' % (Configuration)
	print('AntCMD: '+AntCMD)
	projectCount = 0
	if 1:
		for dir in dirVec:
				androidDir = dir
				print('---------开始Update---------')
				print('所在目录：'+androidDir)
				projectCount += 1
				if 1:
					os.chdir(androidDir)
					os.system(UpdateCMD)
					#依据mk文件相对路径决定是否要进入jni目录
					os.chdir('jni')
					print('==========开始编译')
					os.system(NDKBuildCMD)
					os.chdir('../')
					print('==========装包APK')
					os.system(AntCMD)
					print('==========当前处理完成：'+androidDir)
					#os.chdir(curRootDir)
					#print('---------切回主目录---------')
					projectCount += 1
	print('---------恭喜，完成%d个工程编译，已安装到设备---------' %(projectCount))

#MAIN				
WalkDir(curRootDir)
DoBuild()