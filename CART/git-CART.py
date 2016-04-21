# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:51:57 2016

@author: yangzhou
"""
from numpy import *
import operator
#读取文件
def Parser(filename):
    filename=r'F:\git2\Algorithm-and-Data\CART\bikeSpeedVsIq_test.txt'
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

#数据分隔器,第一个包含节点
def Seperate(data,feature,datasplit):
    dataindex=sum(data[:,feature]<=j)
    data1=data[0:dataindex,:]
    data2=data[dataindex:a1,:]
    return data1,data2

#特征集合器,输出此特征的所有取值
def Datasplit(data,feature):
    datalist=[]
    for i in data[:,feature]:
        datalist.append(float(i))
    datasplit=set(datalist)
    return datasplit

#节点选择器
def Selector(data,feature):
    data=mat(data)
    a1,a2=shape(data)
    data=data[argsort(data.A[:,feature])]     #对特征进行排序
    datasplit=Datasplit(data,feature)
    error=inf
    splitword=data[0,0]
    for j in datasplit:
        data1,data2=Seperate(data,feature,j)
        if error>Error(data1,feature)+Error(data2,feature):
            error=Error(data1,feature)+Error(data2,feature)
            splitword=j        
    return splitword

#误差计算器
def Error(data,feature):
    a1=shape(data)[0]
    if a1==0:
        return 0
    elif sum(data[:,feature]!=data[0,feature])==0:
        matyarr=data[0:a1,1]
        matyarr=data[0:a1,1]-mean(matyarr,0)  #直接返回y的方差
        return matyarr.T*matyarr
    else:
        matarr=data[0:a1,0]
        matyarr=data[0:a1,1]
        ymean=mean(matyarr,0)                #对y进行中心化   
        matyarr=data[0:a1,1]-ymean
        mtm=matarr.T*matarr                  #进行回归并计算误差
        if linalg.det(mtm)==0:
            print('线性回归遇到奇异矩阵')
            return 0
        else:
            ceo=mtm.I*(matarr.T*matyarr)
            error=matarr*ceo-matyarr
            error2=error.T*error
            return error2  

#模型器,主要通过建模输出误差
def Model():
    pass

#预剪枝器
def BeforePruning():
    pass

#后剪枝器
def BackPruning():
    pass

#建立模型树回归
def TreeRegression(filename):
    data=Parser(filename)
    data=mat(data)
    





































