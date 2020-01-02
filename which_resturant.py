#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import random


def statistic(seq):
    result = {}
    for i in set(seq):
        result[i] = seq.count(i)
    print(result)


def rand_pick(seq, probabilities):
    global item
    x = random.uniform(0, 1)
    cumprob = 0.0
    for item, item_pro in zip(seq, probabilities):
        cumprob += item_pro
        if x < cumprob:
            break
    return item


choice = {
    1: "小饿",
    2: "古法牛肉面",
    3: "杨国福",
    4: "百年龙袍",
    5: "师傅李",
    6: "吃鸡",
}
size = len(choice)
prob = [0.3, 0.11, 0.14, 0.15, 0.18, 0.12]

# total = []
# print(prob)
# for i in range(10000):
#     total.append(rand_pick(choice.values(), prob))
# statistic(total)

print(rand_pick(choice.values(), prob))
