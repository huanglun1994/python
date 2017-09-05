# -*- coding: utf-8 -*-
"""xxxxx"""
__author__ = 'Huang Lun'
from redis_demo import RedisHelper

obj = RedisHelper()  # 实例化
obj.public('python')  # 把内容发送到频道
