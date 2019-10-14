#!/usr/bin/env python
import xlwt
import os


def open_file(filename):
    contents = []
    with open(filename, 'r') as fo:
        contents = [line.strip('\n').decode('GB2312') for line in fo.readlines()]
    return contents


def add_sheet(wb, sheet_name, contents):
    sheet = wb.add_sheet(sheet_name)
    i = 0
    for content in contents:
        line_list = content.split(":", 1)
        if len(line_list) != 2:
            continue
        sheet.write(i, 0, line_list[0])
        sheet.write(i, 1, line_list[1])
        i += 1


def main():
    work_book = xlwt.Workbook()

    code_contents = open_file("info.txt")
    add_sheet(work_book, 'sheet 1', code_contents)

    message_contents = open_file("message.txt")
    add_sheet(work_book, 'sheet 2', message_contents)

    if os.path.exists('pylint_message.xls'):
        os.remove('pylint_message.xls')
    work_book.save('pylint_message.xls')


if __name__ == '__main__':
    main()
