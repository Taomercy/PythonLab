# -*- coding:utf-8 -*-
import os
import time
import poplib
import email
from email.header import decode_header
#========================================
# 读取Email，获取Email主题
#========================================
def getEmailSubject():
    read = poplib.POP3_SSL('pop.qq.com')
    read.user('taomercy@qq.com')# 邮箱用户名
    read.pass_('khzzxnxhtbephbej')       # 邮箱设置中的客户端授权密码
    allEmails = read.stat() # 读取邮件信息
    topEmail = read.top(allEmails[0], 0) # 获取最新的一封邮件
    tmp = []
    # 解码邮件，存入tmp
    for s in topEmail[1]:
        try:
            tmp.append(s.decode())
        except:
            try:
                tmp.append(s.decode('gbk'))
            except:
                tmp.append(s.decode('big5'))
    message = email.message_from_string('\n'.join(tmp))
    # 获取邮件主题
    subject = decode_header(message['Subject'])
    if subject[0][1]:
        subjectDecode = subject[0][0].decode(subject[0][1])
    else:
        subjectDecode = subject[0][0]
    return subjectDecode
#=========================================
# 检查Email的主题
#=========================================
def checkEmailSubject():    
    while True:
        subject = getEmailSubject()   
        print('check subject ...')
        print('subject is ' + subject)
        if subject == 'reboot':
            os.system('reboot')
            break        
        if subject == 'shutdown':
            os.system('shutdown now')
            break
        if subject == 'check':
            print 'programma ending...'
            break
        time.sleep(10)  # 每10分钟检查一次

if __name__ == '__main__':
    checkEmailSubject()
