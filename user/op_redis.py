#!/usr/bin/env python
# encoding: utf-8


import redis


def set_mobilie_message(mobile, verification_code):
    re = redis.Redis(host='54.223.220.51', port=6379, db=2)
    re.set(mobile, verification_code, seek)
    re.expire(mobile, 60)
    return True

def message_verify():
    re = redis.Redis(host='54.223.220.51', port=6379, db=2)
    return re.get(mobile)
