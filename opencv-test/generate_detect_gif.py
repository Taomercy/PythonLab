#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

import imageio


def create_gif(image_list, gif_name, duration=1.0):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


def generate(dirname):
    store_path = dirname
    image_list = [os.path.join(store_path, image)for image in os.listdir(store_path)]
    gif_name = dirname + ".gif"
    duration = 0.3
    create_gif(image_list, gif_name, duration)


if __name__ == '__main__':
    generate("detect")
    generate("edges")
