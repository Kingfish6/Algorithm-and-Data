用朴素贝叶斯方法来解决邮件分类问题，数据在email文件夹里面

思路整理：
首先建立一个解析器，统计所有文件中的词条，并选取其中的某些词条，输入文件名和字典，输出词条统计列表和次数列表（之后可以对所有文件使用解析器，并截取最终统计列表中的词条）
然后建立一个统计器，输入文件名和词条列表，输出词条次数列表(主要用于测试文件)
然后制作一个朴素贝叶斯分类器，输入测试文件名和词条标签以及次数矩阵，输出分类结果
（由于一开始对算法不熟悉，返工了很多次。返工的时候学到了，有时候添加方法是为了减少命名变量的次数，不然词都被用光了，很难命名了）

写代码时觉察到的决策树算法的缺点和改进点：
1.朴素贝叶斯方法有2个前提：一个是各个特征独立，二个是各个特征同等重要
2.朴素贝叶斯方法对各个单词在各个文档里面出现的数目不敏感，但可以改进，我的算法就改进过；而且朴素贝叶斯方法对各个单词在测试文档里面出现的数目不敏感，同样可以改进


学到的python代码：
1.利用正则表达式切分字符串。先用re.compile编译正则表达式，然后把结果输出到split方法的参数中、
2.对于字符串与其写成下面的形式还不如用%来表示：
    filepath=r'F:\git2\Algorithm-and-Data\NaiveBayes\email'
	hamfilename=filepath+'\ham'+'\\'+str(i)+'.txt'
3.arange(1,8)中不包括8
4.dataframe按列排序：wordlist1=wordlist1.sort_values('times',ascending=False)



