#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
赶火车仿真
一列火车从A站经过B站开往C站，某人每天赶往B站乘这趟火车。已知火车从A站
到B站的运行时间为均值30分钟，标准差为2分钟的正态随机变量。火车大约在
下午1点离开A站。离开时刻频率分布为：
出发时刻（T)    1:00     1:05      1:10
频率            0.7      0.2       0.1
这个人到达B站时的频率分布为：
到达时刻（T)    1:28     1:30    1:32    1:34
频率            0.3      0.4     0.2     0.1
"""
from __future__ import absolute_import, division, unicode_literals

import random
import numpy as np

# 开车时间的仿真测试
s1 = 0
s3 = 0
count = 1000000
for i in range(count):
    s = random.random()
    if s < 0.7:
        s1 += 1
    elif s > 0.9:
        s3 += 1
print(s1 / count, 1 - s1 / count - s3 / count, s3 / count)
# 人到达时刻仿真测试
s1, s2, s3, s4 = 0, 0, 0, 0
for i in range(count):
    s = random.random()
    if s < 0.3:
        s1 += 1
    elif s < 0.7:
        s2 += 1
    elif s < 0.9:
        s3 += 1
    else:
        s4 += 1
print(s1 / count, s2 / count, s3 / count, s4 / count)
# 火车运行时间仿真测试
s = np.random.normal(0, 1, count)
y = []

for i in range(count):
    y.append(2*s[i] + 30)

# 赶上火车的仿真结果
x1 = [random.random() for i in range(count)]
x2 = [random.random() for i in range(count)]
x3 = np.random.normal(0, 1, count)
s = 0
for i in range(count):
    if x1[i] < 0.7:
        T1 = 0
    elif x1[i] < 0.9:
        T1 = 5
    else:
        T1 = 10

    T2 = 30 + 2 * x3[i]
    if x2[i] < 0.3:
        T3 = 28
    elif x2[i] < 0.7:
        T3 = 30
    elif x2[i] < 0.9:
        T3 = 32
    else:
        T3 = 34
    #    print(T3)
    if (T3 < T2 + T1).all():
        s += 1
    continue
print(s / count)
