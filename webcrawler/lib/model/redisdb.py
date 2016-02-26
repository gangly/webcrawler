#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
redis配置

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""
import redis
from webcrawler.conf import redisconf

rdb = None


def get_redis_server():
    """获取redis实例"""
    global rdb
    if not rdb:
        rdb = redis.Redis(host=redisconf.REDIS_HOST, port=redisconf.REDIS_PORT)
    return rdb

