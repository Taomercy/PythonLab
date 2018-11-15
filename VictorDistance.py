#!/usr/bin/env python
from numpy import *
import scipy.spatial.distance as dist
#vector1 = array([1,2,3]) #mat([1,2,3])
#vector2 = array([4,5,6]) #mat([4,5,6])
vector1 = mat([[1,2], [3,4]])
vector2 = mat([[5,6], [7,8]])

def ManhattanDistance():
    print "ManhattanDistance:"
    print sum(abs(vector1-vector2))


def EuclideanDistance():
    print "EuclideanDistance:"
    print sqrt((vector1-vector2)*(vector1-vector2).T)


def ChebyshevDistance():
    print "ChebyshevDistance:"
    v1 = mat([1,2,3,2])
    v2 = mat([4,5,6,7])
    print sqrt(max(abs(v1-v2)))


def AngleCosine():
    print "AngleCosine:"
    try:
        print dot(vector1,vector2)/(linalg.norm(vector1)*linalg.norm(vector2))
    except:
        v1 = vector1.getA()
        v2 = vector2.getA()
        print dot(v1,v2)/(linalg.norm(v1)*linalg.norm(v2))


def HammingDistance():
    matV = mat([[1,1,1,1],[1,0,0,1]])
    smstr = nonzero(matV[0] - matV[1])
    print "HammingDistance:"
    print smstr


def JaccardDistance():
    matV = mat([[1,1,1,1],[1,0,0,1]])
    print "JaccardDistance:"
    print dist.pdist(matV,'jaccard')


if __name__ == '__main__':
    ManhattanDistance()
    EuclideanDistance()
    ChebyshevDistance()
    AngleCosine()
    HammingDistance()
    JaccardDistance()
