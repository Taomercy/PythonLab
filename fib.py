#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
import numpy


def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)


def fabonacii(n):
    assert n >= 0, "n > 0"
    if n <= 1:
        return 1
    else:
        return fabonacii(n-1) + fabonacii(n-2)


def Fibonacci_Matrix_tool(n):
    Matrix = numpy.matrix("1 1;1 0")
    return pow(Matrix, n)


def Fibonacci_Matrix(n):
    result_list = []
    for i in range(0, n):
        result_list.append(numpy.array(Fibonacci_Matrix_tool(i))[0][0])
    return result_list


print(Fibonacci_Matrix(30)[-2]/Fibonacci_Matrix(30)[-1])

