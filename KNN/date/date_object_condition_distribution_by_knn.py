#!/usr/bin/env python
#! -*- coding:utf-8 -*-
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt
#v = mat([[1,2,3,0,6,9,0,0,6,0],[2,0,4,0,6,0,7,8,0,0]])
#print v.shape
#print nonzero(v)
def file2matrix(filename):
    """
    导入训练数据
    :param filename: 数据文件路径
    :return: 数据矩阵returnMat和对应的类别classLabelVector
    """
    fr = open(filename)
    # 获得文件中的数据行的行数
    numberOfLines = len(fr.readlines())
    # 生成对应的空矩阵
    # 例如：zeros(2，3)就是生成一个 2*3的矩阵，各个位置上全是 0 
    returnMat = zeros((numberOfLines, 3))  # prepare matrix to return
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        # str.strip([chars]) --返回移除字符串头尾指定的字符生成的新字符串
        line = line.strip()
        # 以 '\t' 切割字符串
        listFromLine = line.split()
        # 每列的属性数据
        print(listFromLine)
        returnMat[index, :] = listFromLine[0:3]
        # 每列的类别数据，就是 label 标签数据
        classLabelVector.append(listFromLine[-1])
        index += 1
    # 返回数据矩阵returnMat和对应的类别classLabelVector
    return returnMat, classLabelVector


k = 5
#labels = array(['A', 'A', 'C', 'B'])
#dataset = array([[4,3,6],[4,6,8],[7,3,2],[2,5,2]])
dataset, labels = file2matrix('data.txt')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(dataset[:, 0], dataset[:, 1], 15.0*array(labels, dtype='float64'), 15.0*array(labels,dtype='float64'))
plt.show()


size = dataset.shape[0]
inx = array([3, 0, 10.8])
diffMat = tile(inx, (size, 1)) - dataset
#print diffMat
distances = ((diffMat ** 2).sum(axis=1)) ** 0.5
#print distances
sortedDistIndicies = distances.argsort()
#print 'sortedDistIndicies:', sortedDistIndicies
classCount = {}
for i in range(k):
    voteLabel = labels[sortedDistIndicies[i]]
    classCount[voteLabel] = classCount.get(voteLabel, 0) + 1

print(classCount)
sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
print(sortedClassCount[0][0])
