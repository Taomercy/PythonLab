from sympy import symbols, solve, simplify, expand, Poly
import time


def question1():
    # x+y+z=1
    # x^2+y^2+z^2=2
    # x^3+y^3+z^3=3
    # solve x^4+y^4+z^4=?
    start = time.time()

    x, y, z = symbols('x, y, z')

    result = solve([x+y+z-1, x**2+y**2+z**2-2, x**3+y**3+z**3-3], [x, y, z])

    for i in result:
        print(i)

    print("x^4+y^4+z^4:", result[0][0]**4+result[0][1]**4+result[0][2]**4)
    print("span:", time.time()-start)


x, y, z = symbols('x, y, z')
f1 = expand((x**3+y**3+z**3)*(x+y+z))
print(f1)
f2 = expand((x**3+y**3+z**3)*(x+y+z)-(x**4+y**4+z**4))
print(f2)
