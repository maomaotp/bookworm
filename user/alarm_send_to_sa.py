#!/usr/bin/env python
# encoding: utf-8

import time
import requests
import sys, os

import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

last_post_time = 0

from_addr = "sa@5wei.com"
from_addr_passwd = "BBhc7Pkfcwbz3D"

TEST_GROUP_TAG = 5

WECHAT_URL = 'http://internal-lb-wechat-api-1308542672.cn-north-1.elb.amazonaws.com.cn/qy/notify'
TEST_TAG = 0
PRODUCT_JAVA_TAG = 1
PRODUCT_WEB_TAG = 2
EC2_TAG = 3
OPS_DEPLOY_TAG = 4
RDS_TAG = 5
PHP_TAG = 6
PRODUCT_OPS_JAVA_TAG = 7
BETA_JAVA_TAG = 8

AGENT_DICT = [(11, 1), (3, 1), (14, 2), (4, 3), (13, 3), (15, 9), (16, 10), (3, 3), (18, 1)]

TEST_ADDR = ['liuqiang@5wei.com']
DEV_ADDR = ['dev@5wei.com']
OPS_ADDR = ['liuqiang@5wei.com', 'x@5wei.com']
OPS_JVM_ADDR = ['liuqiang@5wei.com', 'wujin@5wei.com', 'x@5wei.com']
WUJIN_ADDR = ['liuqiang@5wei.com', 'wujin@5wei.com']

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def catch_exception(content=None):
    if not content:
        e_type, e_value, e_traceback = sys.exc_info()
        err_message = "type ==> %s\n" % (e_type.__name__)
        err_message += "value ==> %s\n" %(e_value.message)
        err_message += "traceback ==> file name: %s\n" %(e_traceback.tb_frame.f_code.co_filename)
        err_message += "traceback ==> line no: %s\n" %(e_traceback.tb_lineno)
        err_message += "traceback ==> function name: %s\n" %(e_traceback.tb_frame.f_code.co_name)

        post_mail(err_message, 'liuqiang@5wei.com', 'sa', 'liuqiang')
    else:
        post_mail(content, 'liuqiang@5wei.com', 'sa', 'liuqiang')

#控制微信发送消息时间间隔
def get_interval_time():
    global last_post_time
    cur = time.time()
    if ((cur - last_post_time) > 7):
        last_post_time = cur
        return True
    else:
        #last_post_time = cur
        return False

#告警信息发送邮件
def post_mail(content, to_addr, subject='message', from_str='bookworm', to_str='user', att_file=None):
    #msg = MIMEText(content, 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'%s <%s>'%(from_str, from_addr))
    msg['To'] = _format_addr(u'%s <%s>'%(to_str, to_addr))
    msg['Subject'] = Header(u'%s'%subject, 'utf-8').encode()

    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.exmail.qq.com', 25)
        smtp.login(from_addr, from_addr_passwd)

        #添加附件
        if att_file:
            att = MIMEText(content, 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"'%(att_file)
            msg.attach(att)
        else:
            msg.attach(MIMEText(content, 'plain', 'utf-8'))

        smtp.sendmail(from_addr, to_addr, msg.as_string())
        smtp.quit()
    except Exception as e:
        return Flase
