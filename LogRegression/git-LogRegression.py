# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 22:23:19 2016

@author: yangzhou
"""
from numpy import *
#import pandas as pd 
#建立解析器
def Parser(filename):
    file=open(filename,'r')
    filedata=[]
    fileresult=[]
    for line in file:
        line1=line.strip().split('\t')
        a=len(line1)
        line2=[]
        for word in range(a):
            line2.append(float(line1[word]))
        filedata.append(line2[0:a-1])
        fileresult.append(line2[a-1])
    return filedata, fileresult

#simoid函数
def Sigmoid(x):
    return 1/(1+exp(x*(-1)))

#逻辑斯特回归器
def LogRegression(filename):
    filedata, fileresult=Parser(filename)
    times=100
    length=len(filedata[0])
    parameters=zeros(length)
    step=0.001
    for i in range(times):
        for j in range(length):
            k=random.randint(0,length)
            error=fileresult[k]-Sigmoid(dot(filedata[k],parameters))
            parameters=parameters+dot(step,dot(error,filedata[k]))
    return parameters

#逻辑斯特回归分类器
def Classifier(testlist,parameters):
    if dot(testlist,parameters)<=0.5:
        return 0
    else:
        return 1

if __name__=='__main__':
    trainfile=r'F:\git2\Algorithm-and-Data\LogRegression\horseColicTraining.txt'
    testfile=r'F:\git2\Algorithm-and-Data\LogRegression\horseColicTest.txt'
    parameters=LogRegression(trainfile)
    testdata,testresult=Parser(testfile)
    testnumbers=len(testresult)
    testright=0
    for i in range(testnumbers):
        if Classifier(testdata[i],parameters)==testresult[i]:
            testright+=1
    print(float(testright/testnumbers))



