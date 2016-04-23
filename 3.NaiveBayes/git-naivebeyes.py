# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 09:59:19 2016

@author: yangzhou
"""
from numpy import *
import re
import pandas as pd
#import operator
#创建解析器
def Parser(filename,wordlist):
#    filename=r'F:\git2\Algorithm-and-Data\NaiveBayes\email\ham\1.txt'
    file=open(filename,'r',encoding='gbk')
    line=re.split(r'\W*',file.read())
    for line1 in line:
        wordlist[line1]=wordlist.get(line1,0)+1
    return wordlist

#统计测试样本中的词条数量
def Testwords(filename,wordslist):
    testwords={}
    testwords=Parser(filename,testwords)
    testwordscount=sum(list(testwords.values()))
    testlist=[]
    for word in wordslist:
        testlist.append(testwords.get(word,0))
    return testlist,testwordscount

if __name__=='__main__':
    files=23  
    hamwordlist={}
    spamwordlist={}
    wordlist={}
#求出所有的词条
    for i in arange(1,files+1):
        hamfilename=r'F:\git2\Algorithm-and-Data\NaiveBayes\email\ham\%d.txt' %i
        spamfilename=r'F:\git2\Algorithm-and-Data\NaiveBayes\email\spam\%d.txt' %i
        hamwordlist=Parser(hamfilename,hamwordlist)
        spamwordlist=Parser(spamfilename,spamwordlist)        
        wordlist=Parser(hamfilename,wordlist)
        wordlist=Parser(spamfilename,wordlist)
##选出特征
##    hamwordlist=sorted(hamwordlist.items(),key=operator.itemgetter(1))
#    wordlist1=pd.DataFrame()
#    wordlist1['words']=wordlist.keys()
#    wordlist1['times']=wordlist.values()
#    wordlist1=wordlist1.sort_values('times',ascending=False)
#    wordlist2=list(wordlist1.head(100).words)
#    
#    wordlist3=[]
#    wordsnumber=[]
#    for i in arange(1,files+1):
#        hamwordlist1=[]
#        hamwordlist2={}
#        hamfilename=r'F:\git2\Algorithm-and-Data\NaiveBayes\email\ham\%d.txt' %i
#        hamwordlist2=Parser(hamfilename,hamwordlist2)
#        wordsnumber.append(sum(list(hamwordlist2.values())))
#        for word in wordlist2:
#            hamwordlist1.append(int(hamwordlist2.get(word,0)))
#        wordlist3.append(hamwordlist1)
#    for i in arange(1,files+1):
#        spamwordlist1=[]
#        spamwordlist2={}
#        spamfilename=r'F:\git2\Algorithm-and-Data\NaiveBayes\email\spam\%d.txt' %i
#        spamwordlist2=Parser(spamfilename,spamwordlist2)
#        wordsnumber.append(sum(list(spamwordlist2.values())))
#        for word in wordlist2:
#            spamwordlist1.append(int(spamwordlist2.get(word,0)))
#        wordlist3.append(spamwordlist1)
#    wordlist4=pd.DataFrame(wordlist3,columns=wordlist2)
#    
    number=100             #特征数                          
    wordlist1=pd.DataFrame()
    wordlist1['words']=wordlist.keys()
    wordlist1['times']=wordlist.values()
    wordlist1=wordlist1.sort_values('times',ascending=False)
    hamwordcount=sum(list(hamwordlist.values()))
    spamwordcount=sum(list(spamwordlist.values()))
    wordlist1=wordlist1.head(number)
    wordsdata=pd.DataFrame()
    wordsdata['words']=list(wordlist1.words)
    wordsdata['times']=list(wordlist1['times'])
    hamword=[]
    spamword=[]
    for word in wordsdata.words:
        hamword.append(hamwordlist.get(word,0))
        spamword.append(spamwordlist.get(word,0))
    wordsdata['hamwords']=hamword
    wordsdata['spamwords']=spamword

#输入测试数据
    hamtestwords,hamtestwordscount=Testwords(r'F:\git2\Algorithm-and-Data\NaiveBayes\email\spam\16.txt',list(wordsdata.words))
    wordsdata['hamtestwords']=hamtestwords/hamtestwordscount
    wordsdata['hamwords']=(wordsdata['spamwords']+wordsdata['hamwords']+1)/(hamwordcount+1+spamwordcount)
    wordsdata['spamwords']=(wordsdata['spamwords']+1)/(1+spamwordcount)
    wordsdatatest1=wordsdata[wordsdata.hamtestwords!=0]
    pspamwords=1
    phamwords=1
    j=0
    for i in  wordsdatatest1.words:
            pspamwords=list(wordsdatatest1.spamwords)[j]*pspamwords            
            phamwords=list(wordsdatatest1.hamwords)[j]*phamwords
            j+=1
    print(0.5*pspamwords/phamwords)





































