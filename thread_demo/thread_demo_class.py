#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time
from threading import Thread


class CollectionNum(Thread):
    def __init__(self):
        super().__init__()
        self.__db = []
        self.__count = 100
        self.__cost_time = 0.1

    @property
    def db(self):
        return self.__db

    @property
    def count(self):
        return self.__count

    @property
    def cost_time(self):
        return self.__cost_time

    def collection_num(self, db, ip, tl):
        tl.acquire()
        time.sleep(self.cost_time)
        db.append(ip)
        tl.release()

    def run(self):
        start = time.time()
        threads = []
        thread_id = 1
        for i in range(self.count):
            thread_lock = threading.Lock()
            thread = Thread(target=self.collection_num, args=(self.db, i, thread_lock))
            thread.start()
            threads.append(thread)
            thread_id += 1

        for t in threads:
            if t.is_alive():
                t.join()

        print(self.db)
        print("span1:", time.time() - start)


if __name__ == '__main__':
    c = CollectionNum()
    c.run()
