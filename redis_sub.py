# -*- coding: utf-8 -*-
"""xxxxx"""
__author__ = 'Huang Lun'
from redis_demo import RedisHelper

obj = RedisHelper()
redis_sub = obj.subscribe()

while True:
    msg = redis_sub.parse_response()
    print(msg)
    print(type(msg))
