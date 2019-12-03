#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from PIL import ImageGrab
# bbox = (0, 0, 800, 800)
im = ImageGrab.grab(all_screens=True)
im.save('as.png')















