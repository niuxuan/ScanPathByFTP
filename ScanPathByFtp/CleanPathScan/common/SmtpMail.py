#!/usr/bin/env python3
# coding: utf-8
import smtplib
from email.mime.text import MIMEText

class SmtpMail():
    sender = 'yygjtech@30.net'
    receiver = 'niuxuan@30.net'
    subject = '垃圾路径扫描提醒'
    smtpserver = 'smtp.exmail.qq.com'
    password = 's8s0mifs7h5'

    def SendEmail(self,sum1,sum2,value, sec, IP):
        msg = MIMEText('<html>你好!你的手机垃圾路径采集已经完成，谢谢配合！<br/><h2>扫描IP：{4}</h2><h2>扫描耗时：{0}秒</h2><h2>路径总数：{1}</h2><h2>文件总数：{2}</h2><h2>文件大小：{3}MB</h2></html>'.format(sec,sum1,sum2,value/1024/1024,IP), 'html', 'utf-8')
        msg['Subject'] = "垃圾扫描结束提醒"

        smtp = smtplib.SMTP(self.smtpserver,25)
        smtp.set_debuglevel(1)
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.receiver, msg.as_string())
        """
        smtp.docmd("EHLO server")
        smtp.starttls()
        smtp.docmd("AUTH LOGIN")
        # 发送用户名，是base64编码过的，用send发送的，所以要用getreply获取返回信息
        smtp.send(base64.encodestring(self.sender))
        smtp.getreply()
        # 发送密码
        smtp.send(base64.encodestring(self.password))
        smtp.getreply()
        # mail from, 发送邮件发送者
        smtp.docmd("MAIL FROM: <%s>" % self.sender)
        # rcpt to, 邮件接收者
        smtp.docmd("RCPT TO: <%s>" % self.receiver)
        # data命令，开始发送数据
        smtp.docmd("DATA")
        # 发送正文数据
        smtp.send(msg.as_string())
        # 比如以 . 作为正文发送结束的标记
        smtp.send(" . ")
        smtp.getreply()

        smtp.quit()
        """
    def __init__(self, receiver):
        self.receiver = receiver