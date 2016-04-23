对二维点进行二分k均值聚类，并画图
作出的图形非常好看，很满意

思路整理：
首先建立解析器，读取文件数据
然后建立距离方法，定义距离
然后建立k均值分类器
然后建立二分k均值分类器
然后把数据进行分类，并画图

写代码时觉察到的决策树算法的缺点和改进点：
1.二分的时候如果选取边界上距离最远的2个点是不是能得到最优解？
2.我对二分k均值聚类做了一点小改进，就是每次进行二分的时候，有一个参数t1控制取多少次初始点并从中选出最优的
3。二分k均值聚类为什么有个k，原因是如果不加k限制的话，就会无限二分下去，最后每一个聚类点都是原始数据点


学到的python代码：
1.data=[[float(line.strip().split('\t')[i]) for i in range(len(line.strip().split('\t')))] for line in open(filename).readlines()]一行读取文件数据，哈哈
2.如果函数不能修改它内部的参数，那么没有返回值得函数是怎么修改外面的数的？
3.data1=[datasort[b1] for b1 in range(len(datasort)) if datasort[b1]==i]选取列表中等于i的行
4.在python中把矩阵或数组的值赋给别人会直接把它的指针赋给此人，或者说相当于直接在调用方法的地方贴上方法的代码，所以这个方法应该避免对外面变量产生改变
5.复制一个list最好并且最简单的方法就是用内建对象list，当然你也可以用copy模块，不过没有直接用list来得痛快
6.元组（tuple)、数值型（number)、字符串(string)均为不可变对象，而字典型(dictionary)和列表型(list)的对象是可变对象。传递可变对象的时候是传递对这个对象的引用
7.data.min(0)返回data的各列的最小值
8.plt.scatter(fincentre[:,1],fincentre[:,0], marker = 'x', color = 'm')
  plt.scatter(data[:,1],data[:,0], marker = '+', color = 'c')画散点图
9.最好不要追求一行写完，好难阅读和修改


