#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import threadpool


def sayhello(str, a):
    print("Hello", str, a)
    time.sleep(2)

name_list = ['xiaozi','aa','bb','cc']
params = [([name, "gg"], None) for name in name_list]
start_time = time.time()
pool = threadpool.ThreadPool(10)
requests = threadpool.makeRequests(sayhello, params)
[pool.putRequest(req) for req in requests]
pool.wait()
print("%d second" % (time.time()-start_time))
