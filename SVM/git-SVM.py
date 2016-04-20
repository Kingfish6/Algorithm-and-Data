# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:51:31 2016

@author: yangzhou
"""
from numpy import *
#读取文件
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

#构造径向基函数方法
def InnerProduct(A,B,k):
    A=mat(A)
    B=mat(B)
    distanceAB=(A-B)*(A-B).T
    return exp((-1)*distanceAB/float(k*k))
    
#def InnerProduct(A,B,k):
#    A=array(A)
#    B=array(B)
#    distanceAB=sum(A*B)
#    return distanceAB 

#构造约束函数
def constraint(a,H,L):
#求出h和l
    if a>=H:
        return H
    elif a<=L:
        return L
    else:
        return a

#构造内积函数
def InnerProducts(matdata,k):
    a,b=matdata.shape
    K=zeros((a,a))
    for i in range(a):
        for j in range(a):
            K[i,j]=InnerProduct(matdata[i],matdata[j],k)
    return K
    
#随机选取第二个参数
def Randoma2(a1,j):
    k=random.randint(0,a1)
    if k==j:
        k=Randoma2(a1,j)
    return k

#误差函数
def Error(j,parameter,matlabel,K,b):
    error=0
    a1=K.shape[0]
    for k1 in range(a1):
        error+=parameter[k1]*matlabel[k1]*K[k1,j]
    error=error+b-float(matlabel[j])
    return error

#计算LH
def LH(i,j,matlabel,parameter,c):
    if matlabel[i]!=matlabel[j]:
       L=max(0,parameter[j]-parameter[i])
       H=min(c,c+parameter[j]-parameter[i])
    else:
        L=max(0,parameter[j]+parameter[i]-c)
        H=min(c,parameter[j]+parameter[i])
    return L,H

#启发式方法2
def Selector(i,j,parameter,matlabel,K,b,c):
    a1=K.shape[0]
    l=Randoma2(a1,j)
    error2=Error(l,parameter,matlabel,K,b)
    if i!=1:      
        error1=Error(j,parameter,matlabel,K,b)
        for k1 in range(a1):
            if (parameter[k1]>0 and parameter[k1]<c):
                error=Error(k1,parameter,matlabel,K,b)
                a=error1-error
                b=error1-error2                
                if a*a-b*b>0:
                    l=k1
                    error2=error
    return l,error2
    
#构造SVM
def SVM(matdata,matlabel,rotate,c,k,tol):
    b=0
    a1,a2=matdata.shape
    parameter=zeros(a1)
    K=InnerProducts(matdata,k)
    for i in range(rotate):                                                      #进行大的循环
        for j in range(a1):                                                      #第一个参数
            if i==1 or (parameter[j]>0 and parameter[j]<c):                      #启发式方法1
                error1=Error(j,parameter,matlabel,K,b)
                if ((matlabel[j]*error1 < tol) and (parameter[j] < c)) or ((matlabel[j]*error1 > tol) and (parameter[j] > 0)):                   
                    l,error2=Selector(i,j,parameter,matlabel,K,b,c)              #启发式方法2选择第二个参数
                    L,H=LH(j,l,matlabel,parameter,c)
                    parameter1=parameter[j].copy()                                   #保存旧参数模板
                    parameter2=parameter[l].copy()
                    
                    lamb=K[j,j]+K[l,l]-2*K[j,l]                                    #更新2个参数的值和b的值
                    parameter[l]-=matlabel[l]*array(error2-error1)/lamb
                    parameter[l]=constraint(parameter[l],H,L) 
                    parameter[j]+=matlabel[j]*matlabel[l]*(parameter2-parameter[l])
                    
                    b1=b-error1-matlabel[j]*(parameter[j]-parameter1)*K[j,j]-matlabel[l]*(parameter[l]-parameter2)*K[j,l]
                    b2=b-error2-matlabel[l]*(parameter[j]-parameter1)*K[j,l]-matlabel[l]*(parameter[l]-parameter2)*K[l,l]
                    if parameter[j]<c and parameter[j]>0:
                        b=b1
                    elif parameter[l]<c and parameter[l]>0:
                        b=b2
                    else:
                        b=(b1+b2)/2
    return parameter,b
    
#构造分类器
def Classifier(parameter,matdata,matlabel,b,testdata):  
    a1,a2=matdata.shape
    testdata=mat(testdata)
    w=zeros(a2)
    for i in range(a1):
        w+=(parameter[i]*matlabel[i])*matdata[i]
    testlabel=testdata*mat(w).T+b
    if testlabel>0:
        testlabel=1
    else:   testlabel=-1
    return testlabel    

if __name__=='__main__':
    filename=r'F:\git2\Algorithm-and-Data\SVM\testSetRBF.txt'
    filedata, fileresult=Parser(filename)
    matdata=array(filedata)
    matlabel=array(fileresult)
    traindata=matdata[0:89]
    trainlabel=matlabel[0:89]
    testdata=matdata[89:99] 
    testlabel=matlabel[89:99]
    parameter,b=SVM(traindata,trainlabel,5000,500,1.3,0.0001)
    precision=0.00
    for i in range(10):
        if Classifier(parameter,traindata,trainlabel,b,testdata[i])==testlabel[i]:
            precision+=1
    print(precision/10)








