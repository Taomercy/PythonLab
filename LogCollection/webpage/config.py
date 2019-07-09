#!/usr/bin/env python
# -*- coding:utf-8 -*-
import platform
import os
sysstr = platform.system()
home_path = ""
if sysstr == 'Linux':
    home_path = os.environ['HOME']
elif sysstr == 'Windows':
    home_path = os.environ['TEMP']
else:
    print "sysstr:", sysstr
LOG_SAVING_PATH = os.path.join(home_path, 'LogSavingPath')
if not os.path.exists(LOG_SAVING_PATH):
    os.makedirs(LOG_SAVING_PATH)
MODEL_SAVE_PATH = "ModelSave"
if not os.path.exists(MODEL_SAVE_PATH):
    os.mkdir(MODEL_SAVE_PATH)
