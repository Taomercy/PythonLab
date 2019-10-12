#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time


class Parent(object):
    parentAttr = 100

    def __init__(self):
        self.__site = "a"
        print("parent init")

    def parentMethod(self):
        print('parent method')

    def setAttr(self, attr):
        Parent.parentAttr = attr

    def getAttr(self):
        print("parent attr :", Parent.parentAttr)


class Child(Parent):

    def __init__(self):
        print("child init")

    def childMethod(self):
        print('child method')


c = Child()
c.childMethod()
c.parentMethod()
c.setAttr(200)
c.getAttr()

class A:
    def __init__(self):
        print(self)


a = A()
print(hex(id(a)))

b = A()
print(id(b))
print(hex(id(b)))
print(type(id(b)))