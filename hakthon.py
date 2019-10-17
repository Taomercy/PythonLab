#!/usr/bin/env python
# -*- coding:utf-8 -*-
import xlrd
wb = xlrd.open_workbook('search-2019-10-16.xlsx')
sh = wb.sheet_by_index(0)

for i in range(1, sh.nrows):
    res = []
    value = sh.row_values(i)
    res.append(value[0])
    res.append(value[1])
    solution = value[4].split('\n')
    index = solution.index("General solution:")
    res.append(solution[index+1])
    print(res)
