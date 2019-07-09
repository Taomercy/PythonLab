#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import time


def timestamp2time(tmsp):
    print "imput tmsp:", tmsp
    timeArray = time.localtime(tmsp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def time2timestamp(tm):
    timestamp = int(time.mktime(tm.timetuple()))*1000
    return timestamp


def get_timedelta(tm):
    param = {}
    if tm == 'OneDay':
        param['days'] = 1
    if tm == 'OneWeek':
        param['weeks'] = 1
    if tm == 'OneMonth':
        param['days'] = 30
    if tm == 'ThreeMonth':
        param['days'] = 30*3
    if tm == 'ThreeMonth':
        param['days'] = 30*3
    if tm == 'OneYear':
        param['days'] = 365
    if tm == 'All':
        return None
    now = datetime.datetime.now()
    start = now - datetime.timedelta(**param)
    return start


def get_timestampdelta(tm):
    start = get_timedelta(tm)
    if start is None:
        return None
    return time2timestamp(start)

