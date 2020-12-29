#!/usr/bin/env python
# -*- coding:utf-8 -*-
import random
import threading
import time
from threading import Thread

count = 100
cost_time = [0.01, 0.02, 0.03, 0.5]


def collection_ip(db, ip, threadLock):
    cost = random.choice(cost_time)
    time.sleep(cost)
    threadLock.acquire()
    db.append({ip: cost})
    threadLock.release()


def main1():
    database = []
    threads = []
    threadID = 1

    start = time.time()
    threadLock = threading.Lock()
    for i in range(count):
        ip = i
        thread = Thread(target=collection_ip, args=(database, ip, threadLock))
        thread.start()
        threads.append(thread)
        threadID += 1

    for t in threads:
        if t.is_alive():
            t.join()

    print(database)
    print("span1:", time.time() - start)


def main2():
    res = []
    start = time.time()
    for i in range(count):
        cost = random.choice(cost_time)
        time.sleep(cost)
        res.append({i: cost})
    print(res)
    print("span2:", time.time() - start)


if __name__ == '__main__':
    main1()
    main2()
