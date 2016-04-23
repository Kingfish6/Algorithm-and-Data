# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 08:04:35 2016

@author: yangzhou
"""
from numpy import *
import matplotlib.pyplot as plt
#一行读取所有文件，哈哈
def Parser(filename):
    data=[[float(line.strip().split('\t')[i]) for i in range(len(line.strip().split('\t')))] for line in open(filename).readlines()]
    return data

#创建距离函数
def Distance(a,b):
    c=a-b
    return float((mat(c)*mat(c).T).A[0])

#选取一次重心迭代至稳定
def OneCentre(centre,data):
    k=shape(centre)[0]
    a1=shape(data)[0]
    error=inf
    derror=True
    while(derror):         #当误差没有变化时，停止迭代
#        计算data中各点到重心的距离
        distance=[[Distance(data[i],centre[j]) for j in range(k)] for i in range(a1)]
        #重新计算重心    
        datasort=[argsort(distance[i])[0] for i in range(a1)]
        error1=0
        for i in range(k):
            data1=[data[b1] for b1 in range(len(datasort)) if datasort[b1]==i]
            dataerror=[distance[b1][i] for b1 in range(len(datasort)) if datasort[b1]==i]
            error1+=sum(dataerror)
            centre[i]=mean(data1,0)
        if error1==error:
            derror=False
        error=error1
    return centre,error

#创建k均值分类器,t1为选取重心次数
def Kmeans(data,k,t1):
    data=mat(data)
    a1,a2=shape(data)
    datamin=data.min(0)
    datamax=data.max(0)
    centre=[]
    for i in range(k):
        centre.append(datamin*(1-i/(k-1))+datamax*(i/(k-1)))
#    centre=data.copy()[:k,:]
    error=inf    
    for t in range(t1):
        random.shuffle(data)
        centre1=data.copy()[0:k,]        
        centre1,error1=OneCentre(centre1,data)
        if error1<error:
            centre=centre1
            error=error1
    return centre,error

#建立二分k均值分类器
def BisectingKmeans(rawdata,k,t1):
    rawdata=mat(rawdata)
    a1=shape(rawdata)[0]                    #计算本来的误差
    centre=mean(rawdata,0)
    distance=[Distance(rawdata[j],centre) for j in range(a1)]
    error=sum(distance)
    fincentre=[]
    centre1,error1=Kmeans(rawdata,2,t1)      #尝试进行二分
    if error1<error and k>=2:                        #二分成功
        distance=[[Distance(rawdata[i],centre1[j]) for j in range(2)] for i in range(a1)]
        datasort=[argsort(distance[i])[0] for i in range(a1)]
        data0=mat([list(rawdata[b1].A[0]) for b1 in range(len(datasort)) if datasort[b1]==0])
        data1=mat([list(rawdata[b1].A[0]) for b1 in range(len(datasort)) if datasort[b1]==1])
#        fincentre.append(list(BisectingKmeans(data0).A[0]))
#        fincentre.append(list(BisectingKmeans(data1).A[0]))
        d1,error2=BisectingKmeans(data0,k/2,t1)
        d2,error3=BisectingKmeans(data1,k/2,t1)
        fincentre.extend(d1)
        fincentre.extend(d2)
        error=error2+error3
    else:
        fincentre.append(list(centre.A[0]))
#    fincentre=mat(fincentre)
    return fincentre,error

if __name__=='__main__':
    filename=r'F:\git2\Algorithm-and-Data\8.bisecting-Kmeans\testSet.txt'
    data=Parser(filename)
    fincentre,error=BisectingKmeans(data,16,10)   
    fincentre=mat(fincentre)
    data=mat(data)
    fig=plt.figure()
    plt.subplot(211)
    plt.scatter(fincentre[:,1],fincentre[:,0], marker = 'x', color = 'm')
    plt.scatter(data[:,1],data[:,0], marker = '+', color = 'c')














