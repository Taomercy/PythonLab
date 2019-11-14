#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy.matlib
import numpy as np

# 全0矩阵
print(np.matlib.zeros((2, 2), dtype=int))
# 全1矩阵
print(np.matlib.ones((2, 2), dtype=float))
# 对角线元素为1， 其他为0
print(np.matlib.eye(n=3, M=4, k=0, dtype=float))
# 创建单位矩阵
print(np.matlib.identity(5, dtype=float))

print("=====================")
# 矩阵内积
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(np.dot(a, b))
# 矩阵点积
print(np.vdot(a, b))
# 矩阵行列式
print(np.linalg.det(a))
# 矩阵求逆
print(np.linalg.inv(a))
# 矩阵求解
print('计算：A^(-1)B：')
print(np.linalg.solve(a, b))
# solve 等价 先逆后内积
print(np.dot(np.linalg.inv(a), b))

