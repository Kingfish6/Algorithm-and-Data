# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:23:10 2016

@author: yangzhou
"""

from numpy import *
import pandas as pd 
from math import log
#读取文件
def Parser(filename):
    lenseslabels=['age','prescript','astigmatic','tearrate','result']
    file=open(filename,'r')
#运用dataframe向其中插入dataframe
#    data=pd.DataFrame(columns=lenseslabels)
#    i=0
#    for line in file.readlines():
#        line1=line.strip().split('\t')
#        a=[]
#        a.append(i)
#        data1=pd.DataFrame(line1,columns=a,index=lenseslabels)
#        data=data.append(data1.T)
#        i+=1
#建立多维列表，然后用字典创建
    rowlist=[]
    for line in file.readlines():
        line1=line.strip().split('\t')
        rowlist.append(line1)   
    data=pd.DataFrame(rowlist,columns=lenseslabels)
    return data
        
#评价器
def Valuer(dataframe):
    calculation={}
    a=0
    resultlength=len(dataframe['result'])
    for result in dataframe['result'].values:
        calculation[result]=calculation.get(result,0)+1
    for result in calculation.values():
        a-=(result/resultlength)*log(result/resultlength,2)
    return a

#分类器
def Classifier(dataframe,feat):
    feats=list(set(dataframe[feat]))
    a=len(feats)
    b=len(dataframe[feat])
    featvalue=zeros(a)
    for i in arange(a):
        featframe=dataframe[dataframe[feat]==feats[i]]
        featvalue[i]=featframe[feat].count()/b*Valuer(featframe)
    return sum(featvalue)   

#最优划分器
def Optimization(dataframe):
    feats=dataframe.columns
    featnumber=len(feats)-1
    featvalues=99999999
    for i in arange(featnumber):
        if featvalues>Classifier(dataframe,feats[i]):
            featclassifier=feats[i]
    return featclassifier

#画树状图
def Tree(dataframe):
#得到表的特征数，如果特征树少于2个，则返回0
    feats=dataframe.columns
    featnumber=len(feats)
#得到表的结果数，如果结果都是一样的，则返回0
    result=list(set(dataframe.result))
    resultnumber=len(result)
#建立一个字典来画树图
    if featnumber < 2:
        return set(result)
    elif resultnumber < 2:
        return set(result)
    else:
        optimizefeat=Optimization(dataframe)
        featresult=list(set(dataframe[optimizefeat]))
        tree={}
        treemid={}
        for feat in featresult: 
            treemid[feat]=Tree(dataframe[dataframe[optimizefeat]==feat].drop(optimizefeat,axis=1))
        tree[optimizefeat]=treemid
        return tree


if __name__=='__main__':
    filename=r'F:\git2\Algorithm-and-Data\DecisionTree\lenses.txt'
    dataframe=Parser(filename)
    tree=Tree(dataframe)
    




































