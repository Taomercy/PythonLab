#!/usr/bin/python
# -*- coding: utf-8 -*-
val = input("please input temperature(like 32F or 32C): ")
if val[-1] in ['C', 'c']:
    f = 1.8 * float(val[0:-1]) + 32
    print('Fahrenheit degree: %.2fF' % f)
elif val[-1] in ['F', 'f']:
    f = (float(val[0:-1]) - 32) / 1.8
    print('Celsius degree: %.2fC' % f)
else:
    print("input error")
