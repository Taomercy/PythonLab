import os
from time import sleep

import win32api
import win32con
import win32gui
import win32ui


def printscreen(x1, y1, x2, y2, filename):
    try:
        hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        # print w,h　　　#图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, x2 - x1, y2 - y1)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从(x1, y1)长宽为(x2 - x1, y2 - y1)的图片
        saveDC.BitBlt((0, 0), (x2 - x1, y2 - y1), mfcDC, (x1, y1), win32con.SRCCOPY)
        if not os.path.exists(os.path.dirname(os.path.abspath(filename))):
            os.makedirs(os.path.dirname(os.path.abspath(filename)))
        saveBitMap.SaveBitmapFile(saveDC, filename)
    except Exception as e:
        print('截图失败,失败原因:{}'.format(e))


def debug():
    sleep(3)
    for i in range(50):
        sleep(0.1)
        printscreen(162, 362, 1164, 923, 'm1/{}.png'.format(i))
    # for i in range(640):
    #     sleep(0.1)
    #     printscreen(162, 362, 1164, 923, 'm2/{}.png'.format(i))


if __name__ == '__main__':
    debug()
