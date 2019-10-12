#!/usr/bin/env python
# -*- coding:utf-8 -*-

a, b, *rest = range(5)

print(a)
print(b)
print(rest)

print("===")

first, *mid, last = range(10)

print(first)
print(mid)
print(last)


def func(a, b, *args):
    print(1)


def func(*args):
    a, b, *args = args
    print(2)


func(2, 2)