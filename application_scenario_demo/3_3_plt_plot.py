#!/usr/bin/env python
#! -*- coding:utf-8 -*-
from pylab import *

x = np.linspace(0, 5, 10)
y = x ** 2
fig = plt.figure()
plot(x, y, 'r')
xlabel('x')
ylabel('y')
title('title')
show()


subplot(1, 2, 1)
plot(x, y, 'r^-')
subplot(1, 2, 2)
plot(y, x, 'g*-')
show()