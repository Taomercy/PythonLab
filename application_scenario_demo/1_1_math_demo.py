#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division

a, b = 2, 1/2
print("a = {}, b = {}".format(a, b))
print("a + b = {}".format(a + b))
print("a - b = {}".format(a - b))
print("a * b = {}".format(a * b))
print("a / b = {}".format(a / b))
print("a^b = {}^{} = {}".format(a, b, a**b))
print("a^(-b) = {}^(-{}) ={}".format(a, b, a**-b))

print("===============================")
import math
print("a^(-1/2) = {}".format(math.sqrt(a)))
print("log(a)/log(b) = log({})/log({}) = {}".format(a, b, math.log(a, b)))
print("exp(a) = exp({}) = {}".format(a, math.exp(a)))
print("sin(a) = sin({}) = {}".format(a, math.sin(a)))

