#！usr/bin/python
#!-*- coding:utf-8 -*-
import numpy as np
import os

def csv_reader(csv_file):
    data = []
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as file:
            import csv
            reader = csv.reader(file)
            for line in reader:
                data.append(line)
    return data

class DataUtil():
    def __init__(self, csv_file):
        self.csv_data = csv_reader(csv_file)
    #定义一个方法使其能从文件中读取数据
    #该方法接受4个参数：数据集文件名、训练样本数、类别所在列、是否打乱数据
    def get_dataSet(self, train_num=None, tar_idx=None, shuffle=True):
        x = self.csv_data
        #默认打乱数据
        #if shuffle:
        np.random.shuffle(x)
        #默认类别在最后一列
        tar_idx = -1 if tar_idx is None else tar_idx
        y = np.array([xlist.pop(tar_idx) for xlist in x])
        x = np.array(x)
        #默认全都是训练样本
        if train_num is None:
            return x, y
        #若传入了训练样本数，则依之将数据集切分为训练集和测试集
        return (x[:train_num], y[:train_num]),(x[train_num:], y[train_num:])