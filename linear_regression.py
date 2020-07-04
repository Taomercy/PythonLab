from matplotlib.pyplot import plotting
from numpy import array
import sympy

data = array([
    [1.2, 3.6],
    [2.3, 4.6],
    [1.8, 7.6],
    [5.4, 15.8],
])
k = sympy.Symbol('k')
b = sympy.Symbol('b')
loss = sympy.Symbol('loss')
for i in data:
    loss += (i[1] - (k*i[0] + b))**2
dlossdk = sympy.diff(loss, k)
dlossdb = sympy.diff(loss, b)
print("dlossdk:", dlossdk)
print("dlossdb:", dlossdb)
res = sympy.solve([dlossdk, dlossdb], [k, b])
plotting(res)

