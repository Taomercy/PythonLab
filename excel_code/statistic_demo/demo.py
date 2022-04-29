from openpyxl import load_workbook

work_book_name = "failed_test_suits.xlsx"

workbook = load_workbook(work_book_name)
sheet_ts_slave = workbook['TestSuit-Slave']
try:
    sheet_slaves_count = workbook['Slaves-Count']
except:
    sheet_slaves_count = workbook.create_sheet('Slaves-Count', 4)


def get_row(name, sheet):
    for i in range(sheet.max_row):
        if name == sheet.cell(i + 2, 1).value:
            return i + 2
    return sheet.max_row


def get_column(name, sheet):
    for i in range(sheet.max_column):
        if name == sheet.cell(1, i + 2).value:
            return i + 2
    return sheet.max_column


for slave_row in range(2, sheet_ts_slave.max_row+1):
    slaves = []
    ts_name = sheet_ts_slave.cell(slave_row, 1).value
    for col in range(2, sheet_ts_slave.max_column+1):
            slave = sheet_ts_slave.cell(slave_row, col).value
            slaves.append(slave)

    count = {}
    for slave in slaves:
        if slave:
            if count.get(slave):
                count[slave] += 1
            else:
                count[slave] = 1

    print(ts_name, count)
    count_row = get_row(ts_name, sheet_slaves_count)
    sheet_slaves_count.cell(count_row, 1).value = ts_name
    for s, c in count.items():
        count_column = get_column(s, sheet_slaves_count)
        sheet_slaves_count.cell(1, count_column).value = s
        sheet_slaves_count.cell(count_row, count_column).value = c


workbook.save(work_book_name)