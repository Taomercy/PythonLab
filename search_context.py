#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

# 搜索包含的关键字
keyword = ['hss', 'import']

# 搜索不包含的关键字
exclude_word = ['dog']

# 设定一组指定的文件名扩展，用list方便添加其他类型文件
file_name_list = ['.v', '.txt', '.cpp']

# 设定一组不搜索的文件名
exclude_file_name_list = []


# 定义search函数，便于递归从文件中搜索关键字
def search(search_path):
    # 判断文件路径是否存在
    if os.path.exists(search_path):
        # 获取search_name目录下的文件/文件夹名，并遍历文件
        for file_name in os.listdir(search_path):
            full_path = os.path.join(search_path, file_name)
            # flag 文件名是否包含file_name_list，不包含exclude_file_name_list
            flag = False
            # flag_path 第一次打印文件名
            flag_filepath = True
            i = 0
            # 判断是否是文件
            ################
            ###	非常重要  ######
            ########################
            ####这里一定要用full_path，而不是file_name,否则出错
            if os.path.isfile(full_path):
                # 判断文件名中是否包含指定文件名
                for extend in file_name_list:
                    if extend in file_name:
                        flag = True
                        # 判断文件名中是否不包含exclude_file_name_list中的文件名
                        for exclude in exclude_file_name_list:
                            if exclude in file_name:
                                flag = False
                # 如果flag为真，逐行检索文件中的内容
                if flag:
                    flag = False
                    ff = open(full_path, 'r')
                    # 逐行读取文件内容，防止碰到大的文件卡死
                    for line in ff:
                        i += 1
                        # 是否打印改行标志位FLAG
                        FLAG = False
                        if len(exclude_word) == 0:
                            for KEY in keyword:
                                if KEY in line:
                                    # 改行满足要求，打印
                                    FLAG = True
                                    break
                        else:
                            for KEY in keyword:
                                if KEY in line:
                                    FLAG = True
                                    break
                            for UKEY in exclude_word:
                                if UKEY in line:
                                    FLAG = False
                                    break
                        if FLAG:
                            FLAG = False
                            # 文件路径只输出一次，
                            if flag_filepath:
                                print("file path: " + full_path)
                                flag_filepath = False
                            print("line %d" % i)
                            print(line)
            # 如果是文件夹,递归调用search函数
            ################
            ###	非常重要  ######
            ########################
            ####这里一定要用full_path，而不是file_name,否则出错
            if os.path.isdir(full_path):
                search(full_path)
    else:
        print(search_path, " not path ")


search_path = os.getcwd()
print(search_path)
search(search_path)
