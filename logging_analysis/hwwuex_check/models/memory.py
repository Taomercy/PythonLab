#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
import numpy as np
from matplotlib import pyplot as plt
from application.server.object import Properties
from hwwuex_check.utils.utils import write_yaml

plt.rcParams.update({'font.size': 14})


def calculate_free_memory(memFree, buffers, cached, shmem, sreclaimable):
    return memFree + buffers + cached - shmem + sreclaimable


def get_data(filename):
    data = {}
    with open(filename, 'r') as fr:
        context = fr.read()

        cluster = re.findall(r'\w{2}-\d+', context)
        MemFree = re.findall(r'MemFree:\s+(.*?) kB', context)
        Buffers = re.findall(r'Buffers:\s+(.*?) kB', context)
        Cached = re.findall(r'\nCached:\s+(.*?) kB', context)
        Shmem = re.findall(r'Shmem:\s+(.*?) kB', context)
        SReclaimable = re.findall(r'SReclaimable:\s+(.*?) kB', context)

        for cluster, memfree, buffer, cached, shmem, sreclaimable in \
                zip(cluster, MemFree, Buffers, Cached, Shmem, SReclaimable):
            data.update({cluster: [int(memfree), int(buffer), int(cached), int(shmem), int(sreclaimable)]})

    return data


def get_total_memory(filename):
    with open(filename, 'r') as fr:
        context = fr.read()
        MeMTotal = re.findall(r'MemTotal:\s+(.*?) kB', context)
        if MeMTotal:
            return [int(m) for m in MeMTotal][0]
    return None


def get_plot_size(all):
    if all <= 0:
        return 0, 0
    if all > 0 and all < 4:
        x, y = 1, all
    elif all == 4:
        x, y = 2, 2
    elif all > 4 and all <= 6:
        x, y = 2, 3
    elif all > 6 and all <= 9:
        x, y = 3, 3
    elif all > 9:
        y = 4
        if all % y == 0:
            x = int(all / y)
        else:
            x = int(all / y) + 1
    return x, y


# external interface
def check(log_path, output, **kwargs):
    properties = Properties()
    return_code = "SUCCESS"
    output_log = os.path.join(output, "free_memory.log")
    if os.path.exists(output_log):
        os.remove(output_log)
    fw = open(output_log, "a+")
    fw.write("Start to check free memory.\n")
    pre_log = os.path.join(log_path, "PRE", "memory_full_info.txt")
    pre_data = get_data(pre_log)

    post_log = os.path.join(log_path, "POST", "memory_full_info.txt")
    post_data = get_data(post_log)

    total_memory = get_total_memory(post_log)

    label = ["MemFree", "Buffers", "Cached", "Shmem", "SReclaimable"]

    logger = kwargs.get("summary_log")

    memory_data = {}
    count = 1
    cluster_number = len(pre_data.keys())
    row, column = get_plot_size(cluster_number)
    if row < 4:
        fig = plt.figure(figsize=(20, 4 * column))
    else:
        fig = plt.figure(figsize=(24, 8 + 4 * column))
    fig.suptitle("rate = (V(post) - V(pre)) / M(total)", y=1, fontweight='black')
    for cluster in pre_data.keys():
        # calculate
        pre_value = pre_data[cluster]
        post_value = post_data[cluster]

        pre_memory = calculate_free_memory(*tuple(pre_value))
        post_memory = calculate_free_memory(*tuple(post_value))
        delta_memory = post_memory - pre_memory

        pre_value[3] = -pre_value[3]
        post_value[3] = -post_value[3]
        delta_list = [(post - pre) for pre, post in zip(pre_value, post_value)]
        rate_list = [(post - pre) / pre_memory if pre_memory != 0 else 0.0 for pre, post in
                     zip(pre_value, post_value)]

        free_memory_delta_rate = (delta_memory / pre_memory) * 100
        check_standard_point = abs(free_memory_delta_rate - rate_list[3] * 100)

        if check_standard_point > properties.get_value("free_memory_rate", key=float):
            subtitle = "[%s] Decrement: %.3f%% [FAILED]" % (cluster, free_memory_delta_rate)
            message = "[%s] Decrement: %.3f%% [FAILED] (DEC result is delta/Free_Memory PRE)" % (
                cluster, free_memory_delta_rate)
            fw.write(message + "\n")
            return_code = "FAILED"
        else:
            subtitle = "[%s] Decrement: %.3f%% [SUCCESS]" % (cluster, free_memory_delta_rate)
            message = "[%s] Decrement: %.3f%% [SUCCESS] (DEC result is delta/Free_Memory PRE)" % (
                cluster, free_memory_delta_rate)
            fw.write(message + "\n")

        maximum_value = max(rate_list, key=abs)
        max_type = len(str(maximum_value))
        # output to file
        print("Phase:", end='\t', file=fw)
        print("{str:<{len}}".format(str="Free_Memory", len=max_type), end='', file=fw)
        for l in label:
            print("{str:<{len}}".format(str=l, len=max_type), end='', file=fw)
        print("{str:<{len}}".format(str="(Unit)", len=max_type), file=fw)
        print("PRE:", end='\t', file=fw)
        print("{str:<{len}}".format(str=pre_memory, len=max_type), end='', file=fw)
        for v in pre_value:
            print("{str:<{len}}".format(str=str(v), len=max_type), end='', file=fw)
        print("{str:<{len}}".format(str="(KB)", len=max_type), file=fw)
        print("POST:", end='\t', file=fw)
        print("{str:<{len}}".format(str=post_memory, len=max_type), end='', file=fw)
        for v in post_value:
            print("{str:<{len}}".format(str=str(v), len=max_type), end='', file=fw)
        print("{str:<{len}}".format(str="(KB)", len=max_type), file=fw)
        print("Delta:", end='\t', file=fw)
        print("{str:<{len}}".format(str=delta_memory, len=max_type), end='', file=fw)
        for v in delta_list:
            print("{str:<{len}}".format(str=str(v), len=max_type), end='', file=fw)
        print("{str:<{len}}".format(str="(KB)", len=max_type), file=fw)
        print("DEC:", end='\t', file=fw)
        print("{str:<{len}}".format(str="%.3f%%" % (free_memory_delta_rate), len=max_type), end='', file=fw)
        for v in rate_list:
            print("{str:<{len}}".format(str="%.3f%%" % (v * 100), len=max_type), end='', file=fw)
        print("", file=fw)
        print("=============================================================================================", file=fw)

        # plot
        ax = fig.add_subplot(row, column, count)
        title = subtitle
        ax.set_title(title)
        ax.set_ylabel("size (KB)")
        ax.grid(True)
        ax.set_ylim([-total_memory * 0.2, total_memory * 1.2])
        x = np.arange(len(label))
        width = 0.35
        ax.bar(x - width / 2, pre_value, width=width, align='edge', color='red', alpha=1, label="PRE", tick_label=label)
        ax.bar(x + width / 2, post_value, width=width, align='edge', color='blue', alpha=1, label="POST",
               tick_label=label)
        for rate, pre, post, l in zip(rate_list, pre_value, post_value, x):
            if pre > 0:
                y = pre if pre > post else post
                ax.text(l + width / 2, y, "%.2f%%" % float(rate * 100), ha='center', va='bottom')
            else:
                y = post if pre > post else pre
                ax.text(l + width / 2, y, "%.2f%%" % float(rate * 100), ha='center', va='top')
        ax.legend(loc='upper right')

        # sort data
        pre_value.append(pre_memory)
        post_value.append(post_memory)
        delta_list.append(delta_memory)
        rate_list = ["%.3f%%" % float(rate * 100) for rate in rate_list]
        memory_data[cluster] = [{"PRE": pre_value}, {"POST": post_value}, {"delta": delta_list}, {"rate": rate_list}]
        count += 1

    fw.close()
    display_path = Properties().display_path
    fig.tight_layout()
    fig_save_path = os.path.join(display_path, "free_memory.png")
    fig.savefig(fig_save_path)

    memory_yaml = os.path.join(display_path, "memory.yaml")
    write_yaml(memory_yaml, memory_data)

    logger.info("Check free_memory	: " + return_code)
    #    if return_code == "FAILED":
    #        logger.error("Memory is out of tolerance, check detail in free_memory.log")

    return return_code, output_log
