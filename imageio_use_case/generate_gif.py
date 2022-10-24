#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from functools import cmp_to_key
import imageio.v2 as imageio


def create_gif(image_list, gif_name, duration=1):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
        print(image_name)
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


def mycmp(a, b):
    na = int(os.path.basename(a).split(".")[0])
    nb = int(os.path.basename(b).split(".")[0])
    if na > nb:
        return 1
    elif na < nb:
        return -1
    else:
        return 0


def main():
    store_path = "m1"
    image_list = [os.path.join(store_path, image)for image in os.listdir(store_path)]
    image_list = sorted(image_list, key=cmp_to_key(mycmp))
    gif_name = 'm1.gif'
    duration = 0.1
    create_gif(image_list, gif_name, duration)


if __name__ == '__main__':
    main()
