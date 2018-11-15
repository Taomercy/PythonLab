#!/usr/bin/env python
import xlwt
import os


def prepare_msg_list():
    filename = "pylint_messages_list.log"
    result = []
    with open(filename, 'r') as fo:
        contents = [line.strip('\n') for line in fo.readlines()]
    for line in contents:
        temp_list = []
        if not line.startswith(':'):
            continue
        try:
            codes = line.split(":", 2)[1]
            description = line.split(":", 2)[2]
        except Exception:
            continue
        temp_list.append(codes.split(' ')[0])
        temp_list.append(codes.split(' ')[1].strip('(').strip(')'))
        temp_list.append(description.strip(' *'))
        result.append(temp_list)
    return result


def main():
    contents = prepare_msg_list()
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet('sheet 1')
    i = 0
    for content in contents:
        sheet.write(i, 0, content[1])
        sheet.write(i, 1, content[0])
        sheet.write(i, 2, content[2])
        i += 1
    work_book.save('pylint_message_code.xls')


if __name__ == '__main__':
    main()