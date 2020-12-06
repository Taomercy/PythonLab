import cv2 as cv
import numpy as np

path = 'lr.jpg'
img = cv.imread(path)
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
#cv.imshow('gray', gray)
imgCanny = cv.Canny(gray, 400, 600)
cv.imshow('Canny', imgCanny)
lines = cv.HoughLines(imgCanny, 1, np.pi / 180, 80)
for line in lines:
    rho, theta = line[0]  # line[0]存储的是点到直线的极径和极角，其中极角是弧度表示的。
    a = np.cos(theta)  # theta是弧度
    b = np.sin(theta)
    x0 = a * rho  # 代表x = r * cos（theta）
    y0 = b * rho  # 代表y = r * sin（theta）
    x1 = int(x0 + 1000 * (-b))  # 计算直线起点横坐标
    y1 = int(y0 + 1000 * a)  # 计算起始起点纵坐标
    x2 = int(x0 - 1000 * (-b))  # 计算直线终点横坐标
    y2 = int(y0 - 1000 * a)  # 计算直线终点纵坐标    注：这里的数值1000给出了画出的线段长度范围大小，数值越小，画出的线段越短，数值越大，画出的线段越长
    cv.line(imgCanny, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 点的坐标必须是元组，不能是列表。
cv.imshow("image-lines", imgCanny)
cv.waitKey(0)