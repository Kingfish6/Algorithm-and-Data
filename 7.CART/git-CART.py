# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:51:57 2016

@author: yangzhou
"""
from numpy import *
import re
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

#数据分隔器,第一个包含节点
def Seperate(data,feature,datasplit):
    a1=shape(data)[0]
    dataindex=sum(data[:,feature]<=datasplit)
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

#节点选择器,输出最佳分隔节点
def Selector(data,feature,number,k):
    data=mat(data)
    a1,a2=shape(data)
    data=data[argsort(data.A[:,feature])]     #对特征进行排序
    datasplit=Datasplit(data,feature)
    error=inf
    splitword=inf                             #当splitword是无限大的话，表示不分割
    splitdata1=[]
    splitdata2=[]
    for j in datasplit:
        data1,data2=Seperate(data,feature,j)
        if BeforePruning(data1,data2,number): #满足预剪枝条件才剪枝
            if error-Error(data1,feature)-Error(data2,feature)>k:
                error=Error(data1,feature)+Error(data2,feature)
                splitword=j
                splitdata1=data1
                splitdata2=data2
    return splitword,error,splitdata1,splitdata2

#计算线性回归，返回误差和系数
def Regression(data,a1):
    matarr=data[:,0]
    matyarr=data[:,-1]
    ymean=mean(matyarr,0)                   #对y进行中心化   
    matyarr=data[:,-1]-ymean
    mtm=matarr.T*matarr                     #进行回归并计算误差
    if linalg.det(mtm)==0:
        print('线性回归遇到奇异矩阵')        #解不出模型的话，返回无穷大
        return [],mat(inf*ones(a1)).T,inf   #ymean==inf则表示遇到奇异矩阵
    else:
        ceo=mtm.I*(matarr.T*matyarr)
        error=matarr*ceo-matyarr    
    return ceo,error,ymean

#误差计算器
def Error(data,feature):
    a1=shape(data)[0]
    if a1==0:
        return 0
    elif sum(data[:,feature]!=data[0,feature])==0:
        matyarr=data[:,-1]
        matyarr=data[:,-1]-mean(matyarr,0)  #直接返回y的方差
        return matyarr.T*matyarr
    else:
#        ceo=Regression(data,a1)[0]
        error=Regression(data,a1)[1]
        error2=error.T*error
        return error2  

#预剪枝器
def BeforePruning(data1,data2,number):                      #如果分隔集比较小，则不剪枝
    if shape(data1)[0]<number or shape(data2)[0]<number:
        return False
    else:
        return True

#建立模型树回归,number是分隔集最小个数,误差改变小于k的时候不剪枝
def TreeRegression(data,number,k):
    data=mat(data)
    tree={}
    subtree={}
    a1,a2=shape(data)
    splitfeature=inf                     #对第几个特征剪枝
    splitword=inf                        #剪枝的分隔点
    error=inf                            #误差，无限大则不剪枝
    splitdata1=mat(0)
    splitdata2=mat(0)
    for i in range(a2-1):                #遍历特征查找节点
        splitword1,error1,splitdata11,splitdata22=Selector(data,i,number,k)
        if error-error1>k:
            splitfeature=i
            splitword=splitword1
            splitdata1=splitdata11
            splitdata2=splitdata22
            error=error1
    if splitfeature==inf:                       #如果error==inf则不剪枝
        if sum(data[:,feature]!=data[0,feature])==0:
            return [mat(zeros(a2-1)),mean(data[:,-1],0)]
        else:
            ceo,error,ymean=Regression(data,a1)
            if ymean==inf:
                return ['线性回归遇到奇异矩阵',inf]
            else:
                return [ceo,ymean]
    else:
        subtree1=TreeRegression(splitdata1,number,k)
        subtree2=TreeRegression(splitdata2,number,k)        
        subtree['<%d'%(splitword)]=subtree1
        subtree['>=%d'%(splitword)]=subtree2
        tree[splitfeature]=subtree
    return tree

#后剪枝器
def BackPruning(tree,testingdata,k):
    newtree={}
    newtree1={}
    testingdata=mat(testingdata)
    feature=list(tree.keys())[0]               #取出分类特征和分界值
    subtree1=list(tree.values())[0]
    testingdata=testingdata[argsort(testingdata.A[:,feature])] 
    treevalue=list(subtree1.keys())[0]
    a1=re.match(r'(<(\d+))|(>=(\d+))',treevalue).groups()
    if a1[1]!=None:
        a=a1[1]
    else:
        a=a1[-1]
    a=float(a)
    b1,b2=shape(testingdata)                  #划分数据
    testingdata=testingdata[argsort(testingdata.A[:,feature])]     
    dataindex=sum(testingdata[:,feature]<=a)
    subdata2=testingdata[dataindex:b1,:]
    subtree2=subtree1['>=%d'%a]    
    subdata3=testingdata[0:dataindex,:]
    subtree3=subtree1['<%d'%a]
    if type(subtree2)!=dict or type(subtree3)!=dict:
        error=Error(testingdata,feature)
        error1=Error(subdata2,feature)
        error2=Error(subdata3,feature)   
        if error-error1-error2<k:
            if type(subtree2)==dict:
                return subtree2
            elif type(subtree3)==dict:
                return subtree3
            else:
                ceo,error,ymean=Regression(testingdata,b1)
                return [ceo,ymean]
    else:
        newtree1['>=%d'%a]=BackPruning(subtree2,subdata2,k)
        newtree1['<%d'%a]=BackPruning(subtree3,subdata3,k)
        newtree[feature]=newtree1
        return newtree
   
    
#建立模型解析器，输入数据和树，输出预测值
def Result(tree,matdata):
    feature=list(tree.keys())[0]
    subtree1=list(tree.values())[0]
    treevalue=list(subtree1.keys())[0]
    regression=[]
    a1=re.match(r'(<(\d+))|(>=(\d+))',treevalue).groups()
    if a1[1]!=None:
        a=a1[1]
    else:
        a=a1[-1]
    a=float(a)
    if matdata[feature]>=a:
        subtree2=subtree1['>=%d'%a]
    else:
        subtree2=subtree1['<%d'%a]
    if type(subtree2)!=dict:
        regression=subtree2
    else:
        regression=Result(subtree2,matdata)
    return regression
    
if __name__=='__main__':
    trainingdata=Parser(r'F:\git2\Algorithm-and-Data\CART\bikeSpeedVsIq_train.txt')
    testingdata=Parser(r'F:\git2\Algorithm-and-Data\CART\bikeSpeedVsIq_test.txt')
    tree=TreeRegression(trainingdata,1,1)
    tree2=tree.copy()
    matdata=mat(data[86][0])
    regression=Result(tree,matdata)
    result=matdata*regression[0]+regression[1]
    tree1=BackPruning(tree,testingdata,100000)
    tree2==tree1















