#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys

from PIL import Image


def colorful_to_single(input_img_path, output_img_path):
    """
    彩色图转单色图
    :param input_img_path: 图片路径
    :param output_img_path: 输出图片路径
    """

    img = Image.open(input_img_path)
    # 转化为黑白图片
    img = img.convert("L")
    img.save(output_img_path)


if __name__ == '__main__':
    input_image = sys.argv[1]
    bpath = os.path.dirname(input_image)
    colorful_to_single(input_image, os.path.join(bpath, "output_photo.jpg"))
