#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
dps = range(7)
devisions = range(-3, 4, 1)
x = 261.63


def frequency(x, devision, dp):
    base = (2**devision)*x
    delt = base/12
    return base + delt*dp


for d in devisions:
    for dp in dps:
        print("d={0}, dp={1}, f={2}".format(d, dp, frequency(x, d, dp)))

