#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import re
from wxpy import *
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba


bot = Bot(cache_path=True)
friends = bot.friends()
tList = []
for i in friends:
    signature = i.signature.strip()
    rep = re.compile("<span.*emoji1f\d.+</span>")
    signature = rep.sub("", signature)
    tList.append(signature)

# 拼接字符串
text = "".join(tList)
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)
print(wl_space_split)
my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         max_font_size=40, random_state=42,
                         font_path='c:\\windows\\Fonts\\SimSun-ExtB.ttf').generate(wl_space_split)

plt.figure(figsize=(40, 16), dpi=150)
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
