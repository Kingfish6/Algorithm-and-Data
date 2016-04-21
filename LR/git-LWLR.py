# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:03:25 2016

@author: yangzhou
"""
from numpy import *
import matplotlib.pyplot as plt
#读取文件
def Parser(filename):
    file=open(filename,'r')
    data=[]
    for line in file:
        line=line.strip().split('\t')
        a=len(line)
        line1=[]   
        for word in range(a):
            line1.append(float(line[word]))
        data.append(line1)
    return data

#抽取训练集和测试集
def Selector(data,m):
    random.shuffle(data)
    a1=len(data)
    a2=len(data[0])
    traininglist=[]
    traininglab=[]
    testinglist=[]
    testinglab=[]    
    for i in range(a1):
        if i <int(a1*m):
            traininglist.append(data[i][0:a2-1])
            traininglab.append(data[i][a2-1])
        else:
            testinglist.append(data[i][0:a2-1])
            testinglab.append(data[i][a2-1])
    traininglist=mat(traininglist)
    traininglab=mat(traininglab)
    testinglist=mat(testinglist)
    testinglab=mat(testinglab)
    traininglist=(traininglist-mean(traininglist,0))/var(traininglist,0)
    testinglist=(testinglist-mean(testinglist,0))/var(testinglist,0)
    return traininglist,traininglab,testinglist,testinglab

#核函数
def Kernel(lista,listb,k):
    listc=lista-listb
    return exp(listc*listc.T/(-2)*k**2)

#加权线性回归
def LWLR(testinglist,traininglist,traininglab,k):
    a1=shape(traininglist)[0]
    kernel=eye(a1)
    for i in range(a1):
        kernel[i][i]=Kernel(testinglist,traininglist[i],k)
    mtm=traininglist.T*kernel*traininglist
    if linalg.det(mtm)==0:
        print('数据存在相关性，系数不可求')
    else:
        coe=mtm.I*traininglist.T*kernel*traininglab.T
    return coe

#交叉验证器.m是多少数据用于训练，l是多少个k值
def CrossValidation(data,m,l):
    traininglist,traininglab,testinglist,testinglab=Selector(data,m)
    error=[]
    for j in range(1,l+1):
        k=exp(j-8)
        error1=0
        a1=shape(testinglist)[0]
        for i in range(a1):
            coe=LWLR(testinglist[i],traininglist,traininglab,k)
            error1+=(testinglist[i]*coe-testinglab[0,i])**2
        error.append(float(error1))
    return error

#导入数据并作图
if __name__=='__main__':
    filename=r'F:\git2\Algorithm-and-Data\LR\abalone.txt'
    data=Parser(filename)
    l=8
    error=CrossValidation(data[0:1000],0.85,l)
    error1=(error-mean(error,0))/var(error,0)          #把error进行标准化，作图更容易查看
    karr=range(1,l+1)       
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(karr,error1)
    plt.show()
    
#随便取几个数据回归的试一下
    i=4
    k=exp(argsort(error)[0]-8)
    traininglist,traininglab,testinglist,testinglab=Selector(data[201:401],0.8)
    coe=LWLR(testinglist[i],traininglist,traininglab,k)
    print(float(testinglist[i]*coe))
    print(testinglab[0,i])


