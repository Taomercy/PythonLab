#!/usr/bin/env python
# -*- coding:utf-8 -*-
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED
import time


def spider(page):
    time.sleep(page)
    print(f"crawl task{page} finished")
    return page


with ThreadPoolExecutor(max_workers=5) as t:
    all_task = [t.submit(spider, page) for page in range(1, 5)]
    wait(all_task, return_when=FIRST_COMPLETED)
    print('finished')
    print(wait(all_task, timeout=2.5))

