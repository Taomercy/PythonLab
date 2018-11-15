#!/usr/bin/env python
# -*- coding:utf-8 -*-
from numpy import *
import operator
from TbOperator import *
import sys
import DataBaseInfo
import matplotlib.pyplot as plt

username = DataBaseInfo.username
password = DataBaseInfo.password
dbName = DataBaseInfo.dbName
errorFeatureTb = DataBaseInfo.errorFeatureTb
jobNameTb = DataBaseInfo.jobNameTb
errorTypeTb = DataBaseInfo.errorTypeTb


def matrix_from_mysql(res):
    num = len(res)
    column = len(res[0]) - 1
    returnMat = zeros((num, column))
    classLabelVector = []
    index = 0
    for data in res:
        returnMat[index, :] = data[0:column]
        classLabelVector.append(data[-1])
        index += 1
    return returnMat, classLabelVector


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5

    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def plot_save(dataset, labels, png_name, show=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    coulorA = 15.0 * array(labels, dtype='float64')
    ax.scatter(dataset[:, 2], dataset[:, 1], coulorA, coulorA)
    fig.savefig(png_name, dpi=200)
    print "The picture is saved called:", png_name
    if show:
        plt.show()


def scatter_plot3d(dataset, labels):
    from mpl_toolkits.mplot3d import Axes3D
    coulorA = 15*array(labels, dtype='int')
    ax = plt.subplot(111, projection='3d')
    ax.scatter(dataset[:, 0], dataset[:, 1], dataset[:, 2], coulorA, coulorA, coulorA)
    plt.show()


def error_judge(inX):
    db = DataBase(username, password, dbName)
    res = show_table(db, errorFeatureTb)
    if not res:
        print "%s is not exits" % errorFeatureTb
        sys.exit(0)

    res = data_select(db, errorFeatureTb)

    dataSet, labels = matrix_from_mysql(res)
    plot_save(dataSet, labels)
    #scatter_plot3d(dataset, labels)

    jobId = None
    try:
        jobId = data_select(db, jobNameTb, 'JobName', inX[0], 'id')[0][0]
    except: 
        jobId = data_select(db, jobNameTb, whatSelect='max(id)')[0][0] + 1
    inX[0] = jobId
    inX = array(inX, dtype='float64')
    errorTypeId = classify0(inX, dataSet, labels, 3)
    print "output:", data_select(db, errorTypeTb, 'id', errorTypeId, whatSelect='ErrorString')[0][0]