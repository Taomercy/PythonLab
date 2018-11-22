#!/usr/bin/env python
from __future__ import division
from sympy import symbols, simplify, integrate, limit, oo
x, n = symbols('x, n')
f = x/(1+x)
print "f1 =", f
print "f2 =", simplify(f.subs(x, f))
print "f3 =", simplify(f.subs(x, f).subs(x, f))

fn = x/(n*x+1)
Sn = integrate(fn, (x, 0, 1))
print "Sn =", Sn
print "lim n->oo n*Sn = ", limit(n*Sn, n, oo)
