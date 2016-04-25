# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 17:38:27 2016

@author: yangzhou
"""
from numpy import *
from numpy import linalg as la
import matplotlib.pyplot as plt
#获取数据
file=open(r'F:\git2\Algorithm-and-Data\11.PCA\secom.data','r')
data=[[float(word) for word in line.strip().split(' ')] for line in file]
#数据预处理
data=mat(data)
a1=shape(data)[1]
for i in range(a1):
    datamean=mean(data[nonzero(~isnan(data[:,i]))[0],i])
    data[nonzero(isnan(data[:,i]))[0],i]=datamean
print(all(~isnan(data)))
datamean2=mean(data,0)
data2=data-datamean2
#画图
datacov=cov(data2,rowvar=0)
eigvals,eigvects=linalg.eig(mat(datacov))
eigvects=eigvects.real                     #不知道为什么产生复数了
datasum=[sum(eigvals[:i]) for i in range(len(eigvals))]
datarate=datasum/datasum[-1]
plt.figure(1)
plt.subplot(111)
ind=linspace(1,len(datarate),len(datarate))
plt.plot(ind,datarate)
plt.show()
#数据的空间转换
k=50
datachange=data2*eigvects[:,:k]            #降帷后映射到线性变换空间的矩阵
data3=datachange*eigvects[:,:k].T+datamean2     #降帷后的矩阵
data

































