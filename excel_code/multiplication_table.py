#!/usr/bin/python
#-*- conding:UTF-8 -*-
import xlwt

workbook = xlwt.Workbook(encoding='ascii')
worksheet = workbook.add_sheet('multiplication table')

for i in range(10):
    for j in range(10):
        if i < j:
            continue
        equation = "{0} x {1} = {2}".format(i, j, i*j)
        worksheet.write(i, j, equation)

workbook.save('multiplication_table.xls')
