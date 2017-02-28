
import redis
import random

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse

from .models import UserInfo

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt


def index(request):
    if request.method == 'GET':
        return response_message(code=100001, content='method error!!')
    elif request.method == 'POST':
        return route_message(request)
        #return get_verification_code(request)

def route_message(request):
    '''
    解析字段 op_type 来判断什么操作，进行相应路由
    '''
    params = request.POST
    op_type = params['op_type']

    #获取短信验证码
    if op_type == "1":
        return get_verification_code(params)
        #return response_message(code=100002, content="op_type error!!!")
    elif op_type == "2":
        return is_valid_verification_code(params)
    elif op_type == "3" :
        return save_user_info(params)
    else:
        return response_message(code=100003, content="op_type error!!!")

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

        user = UserInfo(mobile=mobile, nick_name=nick_name, sex=sex, birthday=birthday)
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

        response = sendMessage(mobile)
        save_verification_code(mobile, verification_code)
        if response:
            return response_message(code=0, content=verification_code)
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

def sendMessage(mobile):
    '''
    给用户发送短信验证码
    '''
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
    re.expire(mobile, 120)
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
