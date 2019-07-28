#!user/bin/python
#-*- conding:UTF-8 -*-

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

mail_info = {
	"from":"taomercy@qq.com",
	"to":"1023236042@qq.com",
	"hostname":"smtp.qq.com",
	"username":"taomercy@qq.com",
	"password":"******************",
	"mail_subject":"python mail test",
	"mail_text":"this is a test mail",
	"mail_encoding":"utf-8"
}


def send_mail(mail_info):
	smtp = SMTP_SSL(mail_info["hostname"])
	smtp.set_debuglevel(1)

	smtp.ehlo(mail_info["hostname"])
	smtp.login(mail_info["username"],mail_info["password"])
	msg = MIMEText(mail_info["mail_text"],"plain",mail_info["mail_encoding"])
	msg["Subject"] = Header(mail_info["mail_subject"],mail_info["mail_encoding"])
	msg["From"] = mail_info["from"]
	msg["To"] = mail_info["to"]

	smtp.sendmail(mail_info["from"],mail_info["to"],msg.as_string())
	smtp.quit()


if __name__ == '__main__':
	send_mail(mail_info)
