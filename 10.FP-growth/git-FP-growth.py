# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 09:41:34 2016

@author: yangzhou
"""
from numpy import *
import matplotlib.pyplot as plt
import pandas as pd
#读取dat文件
def Parser(filename):
    data=[line.split() for line in open(filename).readlines()]
    datadict={}
    for line in data:
        datadict[frozenset(line)]=datadict.get(frozenset(line),0)+1
    return datadict

#定义树的节点类
class TreeNode:
    def __init__(self,namevalue,numoccur,parentnode):
        self.name=namevalue
        self.count=numoccur
        self.nodelink=None
        self.parent=parentnode
        self.children={}
        
    def inc(self,numoccur):
        self.count+=numoccur
        
    def disp(self,ind=1):
        print('    '*ind,self.name,' ' ,self.count)
        for child in self.children.values():
            child.disp(ind+1)

#以数据集的频繁项集建立头结点。k是支持度,书上k=100000
def Header(datadict,k):
    header0={}
    header={}
    for item in datadict.keys():
        a=datadict[item]
        for word in list(item):
            header0[word]=header0.get(word,0)+1*a
    for item in header0.keys():
        if header0[item]>k:
            header[item]=header0[item]
    return header

#对记录的排序方法，输入记录，输出排序后的列表
def Itemsort(item,header):
    item1={}
    item3=[]
    for word in header.keys():
        if word in item:
            item1[word]=header[word]
    if item1:
        item2=sorted(item1.items(), key=lambda x:x[1], reverse = True )
        item3=[word[0] for word in item2]
    return item3

#建立fp树
def CreateTree(datadict,k):
    headtree=TreeNode('NullSet',1,None)
    header=Header(datadict.copy(),k)
    headertab={}
    for word in header.keys():
        headertab[word]=None                          #表头的指针方法
    if header=={}:
        print('支持度k太大，频繁集为空集，请重新输入')
    else:
        for item in datadict.keys():
            a=datadict[item]
            itemsort=Itemsort(item,header)            #排序后的item，里面只有频繁集元素，是个列表
            if itemsort!=[]:
                Updatetree(headertab,headtree,itemsort,a,k)    #item是记录，a是记录条数，k是支持度
    return headtree,header,headertab

#指针移动方法，输入表头和节点，把表头最后的指针指向节点
def Headertab(headertab,treenode):
    if type(headertab)==dict:
        if headertab[treenode.name]==None:
            headertab[treenode.name]=treenode
        elif headertab[treenode.name].nodelink==None:
            headertab[treenode.name].nodelink=treenode
        else:
            Headertab(headertab[treenode.name].nodelink,treenode)
    else:
        if headertab.nodelink==None:
            headertab.nodelink=treenode
        else:
            Headertab(headertab.nodelink,treenode)
        
#fp树更新函数，其中item是列表,a是记录条数，k是支持度
def Updatetree(headertab,headtree,item,a,k):
    if headtree.children=={}:
        headtree.children[item[0]]=TreeNode(item[0],a,headtree)
        Headertab(headertab,headtree.children[item[0]])
    elif item[0] in headtree.children.keys():
        headtree.children[item[0]].inc(a)
        if item[1:]!=[]:
            Updatetree(headertab,headtree.children[item[0]],item[1:],a,k)
    else:
        headtree.children[item[0]]=TreeNode(item[0],a,headtree)
        Headertab(headertab,headtree.children[item[0]])

#从一个节点得到它的前缀和前缀数
def Exnode(treenode):
    a=[]
    while(treenode.parent.name!='NullSet'):
        a.append(treenode.parent.name)
        treenode=treenode.parent
    return a

#从fp树中得到item的前缀列表
def Exfp(headertab,item):
    itemdict={}
    item1=headertab[item]
    while(item1!=None):
        if Exnode(item1)!=[]:
            item2=frozenset(Exnode(item1))
            itemdict[item2]=itemdict.get(item2,0)+1*item1.count
        item1=item1.nodelink
    return itemdict

#得出fp频繁集,参数是：数据集,支持度，前缀列表，频繁集
def fpfrequency(datadict,k,exitem,frequencyset):
    headtree,header,headertab=CreateTree(datadict,k)
    for word in header.keys(): 
        a=exitem|frozenset([word])
        frequencyset.add(a)
        itemdict=Exfp(headertab,word)
        if itemdict:
            frequencyset=frequencyset|(fpfrequency(itemdict,k,a,frequencyset))
    return frequencyset

if __name__=='__main__':
    filename=r'F:\git2\Algorithm-and-Data\10.FP-growth\kosarak.dat'
    datadict=Parser(filename)
    frequencyset=fpfrequency(datadict,100000,frozenset(),set([]))




















