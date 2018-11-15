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


subplot(1,2,1)
plot(x, y, 'r^-')
subplot(1,2,2)
plot(y, x, 'g*-')
show()



In [9]: fig = plt.figure()

        axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        # 左侧间距，底部间距，宽度，高度 (从0到1)

        axes.plot(x, y, 'r')

        axes.set_xlabel('x')
        axes.set_ylabel('y')
        axes.set_title('title');
