#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sympy
from numpy import array, arange
import matplotlib.pyplot as plt

gdp = [22460, 11226, 34547, 4851, 5444, 2662, 4549]
consume = [7326, 4490, 11546, 2396, 2208, 1608, 2035]

data = array([
    [22460, 7326],
    [11226, 4490],
    [34547, 11546],
    [4851, 2396],
    [5444, 2208],
    [2662, 1608],
    [4549, 2035],
])


def curve(x, k, b):
    return k*x + b


def main():
    k = sympy.Symbol('k')
    b = sympy.Symbol('b')

    def plotting(paras):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(array(data[:, 0]), array(data[:, 1]))
        x = arange(0, 50000, 50)
        y = curve(x, paras[k], paras[b])
        ax.plot(x, y, 'r')
        plt.show()

    # set y = kx + b
    loss = sympy.Symbol('loss')
    for i in data:
        loss += (i[1] - curve(i[0], k, b)) ** 2

    dlossdk = sympy.diff(loss, k)
    dlossdb = sympy.diff(loss, b)

    # 对k求偏导数
    print("dlossdk:", dlossdk)
    # 对b求偏导数
    print("dlossdb:", dlossdb)

    # 联立方程组求解
    res = sympy.solve([dlossdk, dlossdb], [k, b])
    print("k =", res[k], float(res[k]))
    print("v =", res[b], float(res[b]))
    # 作图
    plotting(res)


if __name__ == '__main__':
    main()
