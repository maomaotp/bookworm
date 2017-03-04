
import redis
import random
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse

from .models import UserInfo


import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt


def index(request):
    if request.method == 'GET':
        return response_message(code=100001, content='method error!!')
    elif request.method == 'POST':
        return route_message(request)
        #return route_message(json.loads(request.body))
        #return get_verification_code(request)

def route_message(request):
    '''
    解析字段 op_type 来判断什么操作，进行相应路由
    '''
    params = eval(request.body)
    #params = request.POST
    op_type = params['op_type']

    #获取短信验证码
    if op_type == "1":
        return get_verification_code(params)
        #return response_message(code=100002, content="op_type error!!!")
    elif op_type == "2":
        return is_valid_verification_code(params)
    elif op_type == "3" :
        return save_user_info(params)
    elif op_type == "4" :
        return log_in(params)
    else:
        return response_message(code=100003, content="op_type error!!!")

def log_in(params):
    mobile = params['mobile']
    passwd = params['passwd']

    #valid_passwd = UserInfo.objects.only('passwd').get(mobile=mobile)
    u = UserInfo.objects.get(mobile=mobile)
    if u.passwd == passwd:
        return response_message(code=0)
    else:
        #return response_message(code=100006, content='passwd error')
        return response_message(code=100006, content=u.passwd)


def save_user_info(params):
    '''
    保存用户信息
    '''
    try:
        mobile = params['mobile']
        nick_name = params['nick_name']
        birthday = params['birthday']
        sex = params['sex']
        passwd = params['passwd']

        user = UserInfo(mobile=mobile, nick_name=nick_name, sex=sex, birthday=birthday, passwd=passwd)
        user.save()
        return response_message(code=0)
    except Exception as e:
        return response_message(code=100005, content=e)



def is_valid_verification_code(params):
    '''
    验证码校验是否正确
    '''
    try:
        mobile = params['mobile']
        captcha = params['captcha']

        valid_captcha = get_valid_captcha(mobile)
        if valid_captcha == captcha:
            return response_message(code=0)
        else:
            return response_message(code=100001, content=str(valid_captcha))
    except Exception as e:
        return response_message(code=100002, content=e)


def get_verification_code(params):
    """
    获取验证码接口
    """
    try:
        mobile = params['mobile']

        verification_code = create_verification_code()

        response = sendMessage(mobile, verification_code)
        save_verification_code(mobile, verification_code)
        if response:
            return response_message(code=0)
        else:
            return response_message(code=100001, content='failed to send message!!')

    except Exception as e:
        return response_message(code=100002, content=e)



def response_message(code, content="ok"):
        responseData = {
            "errcode": code,
            "errmsg": content,
        }

        return JsonResponse(responseData)

def sendMessage(mobile, verification_code):
    '''
    给用户发送短信验证码
    '''
    post_mail(verification_code,'404709954@qq.com')

    return True

def create_verification_code():
    '''
    生成4位验证码
    '''
    temp = ''

    for i in range(4):
        temp += random.choice('0123456789')

    return temp



def save_verification_code(mobile, verification_code):
    """
    redis, update message
    """

    re = redis.Redis(host='54.223.220.51', port=6379, db=2)
    re.set(mobile, verification_code.encode('utf-8'))
    re.expire(mobile, 360)
    return True

def get_valid_captcha(mobile):
    """
    redis, get message_id
    """
    re = redis.Redis(host='54.223.220.51', port=6379, db=2)

    value = re.get(mobile)
    if value:
        return value.decode('utf-8')
    else:
        return False

def post_mail(content, to_addr, subject='message', from_str='bookworm', to_str='user', att_file=None):

    from_addr = "sa@5wei.com"
    from_addr_passwd = "BBhc7Pkfcwbz3D"

    msg = MIMEMultipart()
    #msg['From'] = _format_addr(u'%s <%s>'%(from_str, from_addr))
    msg['From'] = Header("bookworm", 'utf-8')
    #msg['To'] = _format_addr(u'%s <%s>'%(to_str, to_addr))
    msg['To'] = Header("user", 'utf-8')
    #msg['Subject'] = Header(u'%s'%subject, 'utf-8').encode()
    msg['Subject'] = Header(u'%s'%subject, 'utf-8')

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
