#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 定义BlockingScheduler
sched = BlockingScheduler()
sched.add_job(job, 'interval', seconds=5)
sched.start()
