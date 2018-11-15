#！usr/bin/python
#!-*- coding:utf-8 -*-
import os
import sys
import time
from Tree import *
from Util import DataUtil

def main(visualize=True):
    data_obj = DataUtil('example_data.csv')
    x, y = data_obj.get_dataSet()
    fit_time = time.time()
    tree = CartTree(whether_continuous=[False]*4)
    tree.fit(x, y, train_only=True)
    fit_time = time.time() - fit_time
    if visualize:
        tree.view()
    estimate_time = time.time()
    tree.evaluate(x, y)
    x2 = ['紫色','小','小孩','用脚踩']
    tree.evaluat2(x2)


if __name__ == '__main__':
    main(False)