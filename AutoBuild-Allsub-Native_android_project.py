#!/usr/bin/python
# -*- coding: utf-8 -*-
#������������NativeAndroid����
#AutoBuild all sub native android projects
#Zephyr 20141203 Innovation 
import os
import sys

#ָ������Ŀ¼��
targetBuildDir = 'jni' #'Android'
#ָ��Ŀ��Android�汾
targetVersion = 'android-18'
#Build Configuration����ģʽ debug/release
Configuration= 'debug'
#�Ƿ������ϸ������Ϣ
VerbosBuildInfo = 1
#�������������������Ŀ¼���Ͳ������Ա���
blackList = ['obj','res','libs','bin','iOS','src']

#ȫ�ֱ���
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
			print '��  '*(level-1)+'��--'+lists 
			if not lists in blackList:
				if lists == targetBuildDir:
					#print('-----path: '+path) 
					#ȡ�ø���Ŀ¼
					parentDir = os.path.dirname(path) 
					#print('-----parentDir: '+parentDir) 
					dirVec.append(parentDir)
					print('-----��ӱ���Ŀ¼��'+parentDir) 
				else:
					WalkDir(path, level+1) 

def DoBuild():
	print('---------��ʼDoBuild---------')
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
				print('---------��ʼUpdate---------')
				print('����Ŀ¼��'+androidDir)
				projectCount += 1
				if 1:
					os.chdir(androidDir)
					os.system(UpdateCMD)
					#����mk�ļ����·�������Ƿ�Ҫ����jniĿ¼
					os.chdir('jni')
					print('==========��ʼ����')
					os.system(NDKBuildCMD)
					os.chdir('../')
					print('==========װ��APK')
					os.system(AntCMD)
					print('==========��ǰ������ɣ�'+androidDir)
					#os.chdir(curRootDir)
					#print('---------�л���Ŀ¼---------')
					projectCount += 1
	print('---------��ϲ�����%d�����̱��룬�Ѱ�װ���豸---------' %(projectCount))

#MAIN				
WalkDir(curRootDir)
DoBuild()