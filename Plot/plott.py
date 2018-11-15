#!/usr/bin/env python
#! -*- coding:utf-8 -*-
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
def file2matrix(filename, column):

    fr = open(filename)

    numberOfLines = len(fr.readlines())

    returnMat = zeros((numberOfLines, column))  
    classLabelVector = []  
    fr = open(filename)
    index = 0
    for line in fr.readlines():

        line = line.strip()

        listFromLine = line.split()

        returnMat[index, :] = listFromLine[0:column]

        classLabelVector.append(listFromLine[-1])
        index += 1

    return returnMat, classLabelVector


def scatter_plot():
    dataset, labels = file2matrix('data.txt', 3)
    ax = fig.add_subplot(111)
    ax.scatter(dataset[:, 0], dataset[:, 1], 15.0*array(labels, dtype='float64'), 15.0*array(labels,dtype='float64'))
    plt.show()
    #fig.savefig("test1.png", dpi=200)

def scatter_plot3d():
    dataset, labels = file2matrix('data.txt', 4)
    coulorA =  15*array(labels, dtype='int')
    ax = plt.subplot(111, projection='3d')
    ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], coulorA, coulorA, coulorA)
    plt.show()

'''
ax = fig.add_axes([0.0, 0.0, .6, .6], polar=True)
t = linspace(0, 2 * pi, 100)
ax.plot(t, t, color='blue', lw=3);
plt.show()
'''
scatter_plot()
scatter_plot3d()
