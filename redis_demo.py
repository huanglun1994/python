# -*- coding: utf-8 -*-
"""xxxxx"""
__author__ = 'Huang Lun'
import redis


class RedisHelper:
    """类"""
    def __init__(self):
        # 链接
        self.__conn = redis.Redis(host='127.0.0.1')
        self.chan_sub = 'fm104.5'

        # 创建频道
        self.chan__pub = 'fm104.5'

    def public(self, info):
        """公共的"""
        self.__conn.publish(self.chan__pub, info)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.chan_sub)
        pub.parse_response()
        return pub
