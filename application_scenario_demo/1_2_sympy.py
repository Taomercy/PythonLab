#!/usr/bin/env python
'''
known f(x) = x/(1+x), if f1(x) = f(x), f2(x) = f1(f(x)), f3(x) = f2(f(x)),
the area Sn is formed by curve fn(x) and x axis, solve the limit n*Sn when n cross to 'oo'
'''
from __future__ import division
from sympy import symbols, simplify, integrate, limit, oo
x, n = symbols('x, n')


def fnx(n):
    fx = x/(1+x)
    if n == 1:
        fn = fx
    else:
        fn = fnx(n-1).subs(x, fx)
    return simplify(fn)


for i in range(1, 6):
    print("f{0} = {1}".format(i, fnx(i)))
print('...')
print("fn = x/(n*x+1)")
fn = x/(n*x+1)
Sn = integrate(fn, (x, 0, 1))
print("Sn =", Sn)
print("lim(n->oo): n*Sn =", limit(n*Sn, n, oo))
