#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import os
import sys

import xlrd
import xlwt
from xlutils.copy import copy

xl_name = "log_info.xls"
data_sheet_name = "log_info"
label_sheet_name = "log_label"

# alignment = xlwt.Alignment()
# alignment.horz = xlwt.Alignment.HORZ_CENTER
# alignment.vert = xlwt.Alignment.VERT_CENTER
# style = xlwt.XFStyle()
# style.alignment = alignment


def get_data(filename):
    statistic = {}
    with open(filename) as fr:
        context = fr.readlines()

    for line in context:
        if "---" in line:
            error, num = line.strip().split(" --- ")
            if error == "others":
                continue
            statistic[error] = int(num)
    return statistic


def collect_log_info(filename, label=None, training_stat=None):
    if not os.path.exists(xl_name):
        work_book = xlwt.Workbook()
        data_sheet = work_book.add_sheet(data_sheet_name)
        data_sheet.write(0, 0, "log name")
        label_sheet = work_book.add_sheet(label_sheet_name)
        label_sheet.write(0, 0, "log name")
        label_sheet.write(0, 1, "label")
        label_sheet.write(0, 2, "training state")
        work_book.save(xl_name)

    work_book = xlrd.open_workbook(xl_name)
    
    # collect data
    old_data_sheet = work_book.sheet_by_name(data_sheet_name)
    old_nrows = old_data_sheet.nrows
    try:
        old_type_rows = old_data_sheet.row_values(0)
    except:
        old_type_rows = []

    try:
        old_log_cols = old_data_sheet.col_values(0)
    except:
        old_log_cols = []

    log_name = os.path.basename(filename)
    if log_name in old_log_cols:
        print("log has been exist")
        sys.exit()
    old_content = copy(work_book)
    new_data_sheet = old_content.get_sheet(data_sheet_name)
    new_row = old_nrows
    new_data_sheet.write(new_row, 0, log_name)
    data = get_data(filename)

    for key in old_type_rows:
        if key == "log name":
            continue
        if key not in data.keys():
            data[key] = 0

    for key, value in data.items():
        if key in old_type_rows:
            col = old_type_rows.index(key)
            new_data_sheet.write(new_row, col, value)
        else:
            col = len(old_type_rows)
            old_type_rows.append(key)
            new_data_sheet.write(0, col, key)
            for i in range(1, new_row):
                new_data_sheet.write(i, col, 0)
            new_data_sheet.write(new_row, col, value)

    # collect label
    new_label_sheet = old_content.get_sheet(label_sheet_name)
    new_label_sheet.write(new_row, 0, log_name)
    if label:
        new_label_sheet.write(new_row, 1, label)
        new_label_sheet.write(new_row, 2, training_stat)
    else:
        new_label_sheet.write(new_row, 2, training_stat)

    old_content.save(xl_name)


if __name__ == '__main__':
    train_dir = "C:\\Users\\ZIWWUEX\\Desktop\\code\\log_train"
    pre_dir = "C:\\Users\ZIWWUEX\Desktop\code\log_predict"

    files = os.listdir(train_dir)
    for f in files:
        collect_log_info(os.path.join(train_dir, f), label=1, training_stat=True)

    files = os.listdir(pre_dir)
    for f in files:
        collect_log_info(os.path.join(pre_dir, f), label=1, training_stat=False)
