#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time
from threading import Thread
####
database = []


def collection_ip(database, ip, threadLock):
    threadLock.acquire()
    database.append(ip)
    time.sleep(2)
    threadLock.release()


def funcA():
    start = time.time()
    threads = []
    threadID = 1
    for i in range(1000):
        threadLock = threading.Lock()
        ip = "1.1.1.%d" % i
        thread = Thread(target=collection_ip, args=(database, ip, threadLock))
        thread.start()
        threads.append(thread)
        threadID += 1
    # for t in threads:
    #     if t.is_alive():
    #         t.join()

    print("span:", time.time() - start)


if __name__ == '__main__':
    funcA()
    print(database)
