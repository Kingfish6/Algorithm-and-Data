# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 07:05:27 2016

@author: yangzhou
"""

#自己写的Knn算法计算《机器学习实战》第二章的数据
#略微参考《机器学习实战》
from numpy import *
import operator
#建立文件解析器
def Parser(filename):
    file=open(filename,'r')
    labels={'didntLike':1,'smallDoses':2,'largeDoses':3}
    data=[]
    labelvector=[]
    for line in file.readlines():
        line1=line.strip().split('\t')
        a=len(line1)
        if a==4:
            data.append(list(map(lambda x:float(x),line1[:a-1])))
            labelvector.append(int(labels[line1[-1]])) 
        else:
            data.append(list(map(lambda x:float(x),line1[:a-1])))
    if labelvector==[]:
        return data 
    else:
        return data, labelvector
            
#建立分类器
def Classifier(trainingfile,testfile,k):
#    trainingfile=r'F:\git2\Algorithm-and-Data\Knn\datingTrainingSet.txt'
#    testfile=r'F:\git2\Algorithm-and-Data\Knn\datingTestSet.txt'
#    k=1
    trainingdata,traininglabel=Parser(trainingfile)
    testdata,truelabels=Parser(testfile)
    testlabel=[]
    for data1 in testdata:
        distance=[]
        for data2 in trainingdata:
            distance.append(sum((array(data1)-array(data2))**2))
        sortindex=argsort(array(distance))
        labelcount={}
        for i in arange(k):
            labelvalue=traininglabel[sortindex[i]]
            labelcount[labelvalue]=labelcount.get(labelvalue,0)+1
        sortedlabelcount=sorted(labelcount.items(), key=operator.itemgetter(1), reverse = True ) 
        testlabel.append(sortedlabelcount[0][0])
    return sum((array(testlabel)-array(truelabels))==0)/len(testlabel)

if __name__=='__main__':    
    trainingfile=r'F:\git2\Algorithm-and-Data\Knn\datingTrainingSet.txt'
    testfile=r'F:\git2\Algorithm-and-Data\Knn\datingTestSet.txt'
    k=18
    print(Classifier(trainingfile,testfile,k))























