
import redis
import random

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse

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
    try:
        params = request.POST
        op_type = params['op_type']

        #获取短信验证码
        if op_type == "1":
            return get_verification_code(params)
            #return response_message(code=100002, content="op_type error!!!")
        elif op_type == "2":
            return is_valid_verification_code(params)
        else:
            return response_message(code=100003, content="op_type error!!!")

    except Exception as e:
        return response_message(code=100004, content=e)

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


def get_verification_code(params):
    """
    send message to user
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


def save_verification_code(mobile, verification_code):
    """
    redis, update message
    """

    re = redis.Redis(host='54.223.220.51', port=6379, db=2)
    re.set(mobile, verification_code)
    re.expire(mobile, 120)
    return True

def message_verify():
    """
    redis, get message_id
    """
    re = redis.Redis(host='54.223.220.51', port=6379, db=2)
    return re.get(mobile)
