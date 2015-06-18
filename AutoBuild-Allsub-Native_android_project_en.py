#!/usr/bin/python
# -*- coding: utf-8 -*-
#Batch compileNativeAndroid
#AutoBuild all sub native android projects
#Zephyr 20141203
import os
import sys

#Target compile directory
targetBuildDir = 'jni' 
#Target Android version
targetVersion = 'android-18'
#Build Configuration: debug/release
Configuration= 'debug'
#Will output detail compile info
VerbosBuildInfo = 1
#Blacklist for skip-directory 
blackList = ['obj','res','libs','bin','iOS','src']

#Global
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
			print '©¦  '*(level-1)+'©¦--'+lists 
			if not lists in blackList:
				if lists == targetBuildDir:
					#Get parent directory
					parentDir = os.path.dirname(path) 
					dirVec.append(parentDir)
					print('-----add compile directory£º'+parentDir) 
				else:
					WalkDir(path, level+1) 

def DoBuild():
	print('---------Begin DoBuild---------')
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
				print('---------Begin Update---------')
				print('Current directory£º'+androidDir)
				projectCount += 1
				if 1:
					os.chdir(androidDir)
					os.system(UpdateCMD)
					#Rely on make file to decide whether cd into jni directory
					os.chdir('jni')
					print('==========Begin compile')
					os.system(NDKBuildCMD)
					os.chdir('../')
					print('==========building APK')
					os.system(AntCMD)
					print('==========work done on£º'+androidDir)
					#os.chdir(curRootDir)
					#print('---------go back directory---------')
					projectCount += 1
	print('---------Congratulation£¬%d projects compiled£¬and deployed on device---------' %(projectCount))

#MAIN				
WalkDir(curRootDir)
DoBuild()