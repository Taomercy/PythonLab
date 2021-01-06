#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import time
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import cpu_count

from IPython.utils import contexts

workers = (cpu_count() or 1) * 5


def task(id):
    sec = random.choice([0.01, 0.02, 0.5, 10])
    print("task-{} start: {}".format(id, sec))
    time.sleep(sec)
    print("task-{} span: {}".format(id, sec))
    return sec


datas = []
start = time.time()
with ThreadPoolExecutor(max_workers=8) as executor:
    future_obj = {executor.submit(task, number): number for number in range(1, 100)}
    for future in futures.as_completed(future_obj):
        sec = future_obj[future]
        try:
            data = future.result()
            datas.append(data)
        except Exception as exc:
            print('%r generated an exception: %s' % (sec, exc))

print(datas)
print("span:", time.time()-start)
