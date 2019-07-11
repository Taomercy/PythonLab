#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import re

#
# def get_readlines(filename):
#     context = []
#     with open(filename, 'r') as fr:
#         context = [line.strip('\n') for line in fr.readlines()]
#     return context
#
#
# def get_log_string(filename):
#     context = get_readlines(filename)
#     log_string = ""
#     for line in context:
#         log_string += line
#     return log_string
#
#
# def filter_error(context):
#     indexs = []
#     flag = 0
#     for i in range(len(context)):
#         line = context[i]
#         # if re.search(r'Traceback', line, re.M | re.I): flag = 1
#         # if re.search(r'Error:', line): flag = 0
#         if flag or re_error(line):
#             indexs.append(i)
#     return indexs
#
#
# def re_error(line):
#     res = 0
#     if re.search(r'error:', line, re.M | re.I) or\
#             re.search(r'cannot', line, re.M | re.I) or \
#             re.search(r'exception:', line, re.M | re.I) or \
#             re.search(r'failed', line, re.M | re.I) or \
#             re.search(r'Permission denied', line, re.M | re.I) or \
#             re.search(r'marked build as failure', line, re.M | re.I) or \
#             re.search(r'No such file or directory', line, re.M | re.I):
#         res = 1
#     return res


# def get_key_log(filename):
#     context = get_readlines(filename)
#     outputs = filter_error(context)
#     filter_log = []
#     for i in outputs:
#         filter_log.append(context[i])
#     return filter_log


def log_filter(log):
    result = []
    lines = log.split('\n')
    for line in lines:
        if re.search(r'error:', line, re.M | re.I) or \
                re.search(r'cannot', line, re.M | re.I) or \
                re.search(r'failed', line, re.M | re.I) or \
                re.search(r'exception:', line, re.M | re.I) or \
                re.search(r'Permission denied', line, re.M | re.I) or \
                re.search(r'marked build as failure', line, re.M | re.I) or \
                re.search(r'No such file or directory', line, re.M | re.I):
            result.append(line)
    return '\n'.join(result)


def get_filter_log(filename):
    with open(filename, 'r') as fr:
        context = fr.read()
    return log_filter(context)


def get_readlines_log(filename):
    with open(filename, 'r') as fr:
        lines = fr.readlines()
    return lines