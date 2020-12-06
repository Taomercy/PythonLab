#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
#直线检测
#使用霍夫直线变换做直线检测，前提条件：边缘检测已经完成
import math
import sys

import cv2 as cv
import numpy as np
image_path = 'line3.jpg'
# image_path = 'ladder.jpg'

import math

# A(1,-3)B(5,-1)C(4,1)D(4.5,4.5)
# AB = [1,-3,5,-1]
#AB = [5, -1, 1, -3]
#CD = [4, 1, 4.5, 4.5]

def angle(v1, v2):
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180 / math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180 / math.pi)
    # print(angle2)
    if angle1 * angle2 >= 0:
        included_angle = abs(angle1 - angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    return included_angle



# #得到向量的坐标以及向量的模长
# class Point(object):
#     def __init__(self, x1, y1, x2, y2):
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2
#
#     def vector(self):
#         c = (self.x1 - self.x2, self.y1 - self.y2)
#         return c
#
#     def length(self):
#         d = math.sqrt(pow((self.x1 - self.x2), 2) + pow((self.y1 - self.y2), 2))
#         return d
#
# #计算向量夹角
# class Calculate(object):
#     def __init__(self, x, y, m, n):
#         self.x = x
#         self.y = y
#         self.m = m
#         self.n = n
#
#     def Vector_multiplication(self):
#         self.mu = np.dot(self.x, self.y)
#         return self.mu
#
#     def Vector_model(self):
#         self.de = self.m * self.n
#         return self.de
#
#     def cal(self):
#         result = Calculate.Vector_multiplication(self) / Calculate.Vector_model(self)
#         return result


#标准霍夫线变换
def line_detection(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)  #apertureSize参数默认其实就是3
    cv.imshow("edges", edges)
    lines = cv.HoughLines(edges, 1, np.pi/180, 80)
    for line in lines:
        rho, theta = line[0]  #line[0]存储的是点到直线的极径和极角，其中极角是弧度表示的。
        a = np.cos(theta)   #theta是弧度
        b = np.sin(theta)
        x0 = a * rho    #代表x = r * cos（theta）
        y0 = b * rho    #代表y = r * sin（theta）
        x1 = int(x0 + 1000 * (-b)) #计算直线起点横坐标
        y1 = int(y0 + 1000 * a)    #计算起始起点纵坐标
        x2 = int(x0 - 1000 * (-b)) #计算直线终点横坐标
        y2 = int(y0 - 1000 * a)    #计算直线终点纵坐标    注：这里的数值1000给出了画出的线段长度范围大小，数值越小，画出的线段越短，数值越大，画出的线段越长
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)    #点的坐标必须是元组，不能是列表。
    cv.imshow("image-lines", image)

#统计概率霍夫线变换
def line_detect_possible_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    cv.imshow('imggray', gray)
    #cv.imshow('opening', opening)
    edges = cv.Canny(gray, 50, 150, apertureSize=3)  # apertureSize参数默认其实就是3
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength=120, maxLineGap=5)
    result_lines = []
    points = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y1 - y2) < 5:
            continue
        result_lines.append(line)
        print("coordinate:", x1, y1, x2, y2)
        points.append([x1, y1, x2, y2])
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv.imwrite('line_detect_possible.jpg', image)
    cv.imshow("line_detect_possible_demo", image)
    return points



line_detect_possible_demo
# ca = Calculate(first_point.vector(), two_point.vector(), first_point.length(), two_point.length())
# print("angle:", abs(math.degrees(ca.cal())))
cv.waitKey(0)
cv.destroyAllWindows()
