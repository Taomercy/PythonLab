#!/usr/bin/env python
# -*- coding:utf-8 -*-
from wxpy import *
import matplotlib.pyplot as plt


def get_friend_sex(friends):
    male = female = other = 0
    for i in friends[1:]:
        sex = i.sex
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    return male, female, other


bot = Bot(cache_path=True)
friends = bot.friends()

male, female, other = get_friend_sex(friends)
total = len(friends[1:])
my_name = friends[0].nick_name

sex_name = ['male', 'female ', 'other']

sex_count = [male, female, other]

plt.figure(figsize=(20, 9), dpi=100)

plt.pie(sex_count, labels=sex_name, autopct="%.2f%%", colors=['b', 'r', 'g'])

plt.legend()

plt.title('%s friends gender rate from WeChat' % my_name)

plt.axis('equal')

plt.show()
