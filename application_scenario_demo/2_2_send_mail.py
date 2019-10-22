#!/usr/bin/env python
# -*- coding:utf-8 -*-\
import xlrd
import datetime
import time
import sys
import getpass
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
mdict = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
         5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
         9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

br_name = "Wei"

try:
    MONTH = int(sys.argv[1])
    mail_password = getpass.getpass("Please input your email password:")
except Exception as e:
    print(e)
    sys.exit()


class MailTable(object):
    html = None
    table_head = None
    td_head = None

    def __init__(self):
        self.table_head = "<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=756 style='width:567.0pt;margin-left:-.65pt;border-collapse:collapse'>"
        self.td_head = """
                    <td width=64 nowrap valign=bottom style='width:48.0pt;border:solid windowtext 1.0pt;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>HRID<o:p></o:p></span></b></p></td>
                    <td width=96 valign=bottom style='width:1.0in;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>Spell Name<o:p></o:p></span></b></p></td>
                    <td width=119 nowrap valign=bottom style='width:89.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>Chinese Name<o:p></o:p></span></b></p></td>
                    <td width=133 nowrap valign=bottom style='width:100.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>PCODE<o:p></o:p></span></b></p></td>
                    <td width=97 nowrap valign=bottom style='width:73.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>OT Month<o:p></o:p></span></b></p></td>
                    <td width=81 nowrap valign=bottom style='width:61.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>OT Day<o:p></o:p></span></b></p></td>
                    <td width=80 nowrap valign=bottom style='width:60.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>OT hours<o:p></o:p></span></b></p></td>
                    <td width=85 nowrap valign=bottom style='width:64.0pt;border:solid windowtext 1.0pt;border-left:none;background:#17375D;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><b><span style='font-size:10.0pt;font-family:"Arial",sans-serif;color:white'>OT Type<o:p></o:p></span></b></p></td>
        """
        self.html = "<p>Hi,</p><p>My OT info in {0}：</p>".format(mdict[MONTH])
        self.html += self.table_head
        self.html += self.td_head

    def add_tr(self, spell_name, chinese_name, pcode, ot_month, ot_day, ot_hours, ot_type):
        td = """
                    <td width=64 nowrap style='width:48.0pt;border:solid windowtext 1.0pt;border-top:none;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='color:black'>60712<o:p></o:p></span></p></td>
                    <td width=96 nowrap style='width:1.0in;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{0}<o:p></o:p></span></p></td>
                    <td width=119 nowrap style='width:89.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span lang=ZH-CN style='font-size:10.0pt;font-family:SimSun'>{1}</span><span style='font-size:10.0pt;font-family:SimSun'><o:p></o:p></span></p></td>
                    <td width=133 nowrap valign=bottom style='width:100.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='color:black'>{2}</span><span style='font-size:10.0pt;font-family:"Times New Roman",serif'><o:p></o:p></span></p></td>
                    <td width=97 nowrap valign=bottom style='width:73.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal align=center style='text-align:center'><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{3}<o:p></o:p></span></p></td>
                    <td width=81 nowrap valign=bottom style='width:61.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{4}<o:p></o:p></span></p></td>
                    <td width=80 nowrap valign=bottom style='width:60.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{5}<o:p></o:p></span></p></td>
                    <td width=85 nowrap valign=bottom style='width:64.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:#FCD5B4;padding:0in 5.4pt 0in 5.4pt;height:15.65pt'><p class=MsoNormal><span style='color:black'>{6}</span></p></td>
        """.format(spell_name, chinese_name, pcode, ot_month, ot_day, ot_hours, ot_type)
        tr = "<tr style='height:15.0pt'>" + td + "</tr>"
        self.html += tr

    def add_total_tr(self, total):
        td = """            
            <td width=64 nowrap style='width:48.0pt;border:solid windowtext 1.0pt;border-top:none;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'></td>
            <td width=96 nowrap style='width:1.0in;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'></td>
            <td width=119 nowrap style='width:89.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:white;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'></td>
            <td width=133 nowrap valign=bottom style='width:100.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'></td>
            <td width=97 nowrap valign=bottom style='width:73.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'></td>
            <td width=81 nowrap valign=bottom style='width:61.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>Total:<o:p></o:p></span></p></td>
            <td width=80 nowrap valign=bottom style='width:60.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'><p class=MsoNormal><span style='font-size:10.0pt;font-family:"Times New Roman",serif'>{0}<o:p></o:p></span></p></td>
            <td width=85 nowrap valign=bottom style='width:64.0pt;border-top:none;border-left:none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;background:#FCD5B4;padding:0in 5.4pt 0in 5.4pt;height:15.0pt'></td>
        """.format(total)
        tr = "<tr style='height:15.0pt'>" + td + "</tr>"
        self.html += tr

    def get_html(self):
        self.html += '</table>'
        self.html += '<p>BR/{0}</p>'.format(br_name)
        return self.html


def get_delta_time(value):
    date = value.split(' ')[0]
    timedelta = value.split(' ')[1]
    timestart = timedelta.split('-')[0]
    timeend = timedelta.split('-')[1]
    ts = date + ' ' + timestart
    te = date + ' ' + timeend
    timeArray1 = time.strptime(ts, "%m/%d/%Y %H:%M")
    timeStamp1 = int(time.mktime(timeArray1))
    dateArray1 = datetime.datetime.utcfromtimestamp(timeStamp1)

    timeArray2 = time.strptime(te, "%m/%d/%Y %H:%M")
    timeStamp2 = int(time.mktime(timeArray2))
    dateArray2 = datetime.datetime.utcfromtimestamp(timeStamp2)

    delta = dateArray2 - dateArray1
    return date, delta


def get_info(month):
    data = xlrd.open_workbook("201812.xlsx")
    table = data.sheets()[1]
    times = table.col_values(3)
    values = []
    for t in times:
        unit = t.split('\n')
        for u in unit:
            if u.startswith(str(month)):
                values.append(u)
    return values


def send_mail(html):
    mail_info = {
        "from": "wei.wu@cienet.com.cn",
        "to": ["wei.wu@cienet.com.cn"],
        "hostname": "pop.263xmail.com",
        "username": "wei.wu@cienet.com.cn",
        "password": mail_password,
        "mail_subject": "RE: OT hours in {0}".format(mdict[MONTH]),
        "mail_text": html,
        "mail_encoding": "utf-8"
    }

    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)

    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])
    msg = MIMEText(mail_info["mail_text"], _subtype="html", _charset=mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["From"] = mail_info["from"]
    msg["To"] = ",".join(mail_info["to"])
    msg["Cc"] = ",".join(mail_info["cc"])

    smtp.sendmail(mail_info["from"], mail_info["to"] + mail_info["cc"]+["wei.wu@cienet.com.cn"], msg.as_string())
    smtp.quit()


mt = MailTable()
values = get_info(MONTH)
total_time = 0
for value in values:
    date, delta = get_delta_time(value)
    print(date, delta.seconds/60.0/60.0)
    dlist = date.split('/')
    month = dlist[0]
    day = dlist[1]
    hours = delta.seconds/60.0/60.0
    total_time += hours
    mt.add_tr("Wu Wei", "吴威", "ERIC-Shanghai", ot_month=month, ot_day=day, ot_hours=hours, ot_type="Week day")
mt.add_total_tr(total_time)
print("toatal:", total_time)
confirm = input("confirm (yes/no?):")
if confirm == 'yes':
    send_mail(mt.get_html())
else:
    print("quit")
