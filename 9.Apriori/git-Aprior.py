# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 19:25:25 2016

@author: yangzhou
"""
from numpy import *
import matplotlib.pyplot as plt
import pandas as pd
#读取dat文件
def Parser(filename):
    data=[line.split() for line in open(filename).readlines()]
    return data

#找出单字母的频繁集和字典
def Frequency(mushroomdata,items,t):
    a1,a2=shape(mushroomdata)
    frequency={}
    for i in range(a1):
        for j in range(a2):
            frequency[frozenset([mushroomdata[i][j]])]=frequency.get(frozenset([mushroomdata[i][j]]),0)+1
#        del frequency[frozenset({'2'})]
    frequency1={}
    for word in frequency.keys():
        if frequency[word]>=t*items:
            frequency1[word]=frequency[word]
    return frequency1
    
#把数据集分为毒蘑菇集和非毒蘑菇集    
def Classify(data):
    a1,a2=shape(data)
    poison=[]
    nonpoison=[]
    for mushroom in data:
        if mushroom[0]=='2':
            poison.append(mushroom[1:a2])
        else:
            nonpoison.append(mushroom[1:a2])
    return poison,nonpoison

#以某个字典的元素来形成的超集
def Set(datadict):
    datakeys=list(datadict.keys())
    a1=len(datakeys)
    a2=len(datakeys[0])                     #注意datakeys需要为非空集合
    superset=[]    
    for i in range(a1):
        for j in range(i+1,a1):
            if len(datakeys[i]|datakeys[j])==a2+1:
                superset.append(datakeys[i]|datakeys[j]) 
    superset=list(set(superset))
    return superset

#给出数据集和Ck，输出Lk和字典,t是最小支持度
def Frequentset(poison,ck,t,items):
    lk=[]
    ckfrequency={}
    ckfrequency1={}
    for line in poison:
        for word in ck:
            if word.issubset(frozenset(line)):
                ckfrequency[word]=ckfrequency.get(word,0)+1
    for word in ckfrequency.keys():
        if ckfrequency[word]>=t*items:
            ckfrequency1[word]=ckfrequency[word]
    return ckfrequency1

#找出非毒蘑菇中的频繁集次数
def Nonpoison(frequencyall,nonpoison):
    nonfrequencyall={}
    confifence={}
    for line in nonpoison:
        for word in frequencyall.keys():
            if word.issubset(frozenset(line)):
                nonfrequencyall[word]=nonfrequencyall.get(word,0)+1
    for word in frequencyall.keys():
        confifence[word]=frequencyall[word]/(nonfrequencyall.get(word,0)+frequencyall[word])
    return confifence

#输出最后的频繁集并排序，在另一个字典中储存可信度
def Apriori(data,t):
    poison,nonpoison=Classify(data)
    items=len(poison)+len(nonpoison)
    supportance={}
    frequency1=Frequency(poison,items,t)
    number=min(len(poison[0]),len(list(frequency1.values())))
    frequencyall=frequency1
    frequency2=frequency1
    for i in range(2,number+1):
        ck=Set(frequency2)
        ckfrequency1=Frequentset(poison,ck,t,items)
        if not ckfrequency1: break
        frequency2=ckfrequency1
        frequencyall.update(ckfrequency1)
    for word in frequencyall.keys():
        supportance[word]=frequencyall[word]/items
    return frequencyall,supportance

if __name__=='__main__':
    filename=r'F:\git2\Algorithm-and-Data\9.Apriori\mushroom.dat'
    data=Parser(filename)
    t=0.4
    frequencyall,supportance=Apriori(data,t)
    confifence=Nonpoison(frequencyall,nonpoison)
    supportance1=pd.DataFrame(supportance,index=['supportance']).T
    confifence1=pd.DataFrame(confifence,index=['confifence']).T
    supportance1['confifence']=confifence1['confifence']
    supportance1.sort(['confifence'],ascending=False)






















