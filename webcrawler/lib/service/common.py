#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
对公共函数的封装

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""

import os
import time
import random
import commands
from w3lib.html import remove_entities
from urlparse import urljoin

from webcrawler.conf.spiderconf import USER_AGENT_LIST

NULL = [None, 'null']


def now_time(timeformat='%Y-%m-%d %X'):
    """
    get the local now time
    return string
    """
    return time.strftime(timeformat, time.localtime(time.time()))


def gethostname():
    """get host name"""
    sys = os.name
    hostname = 'Unkwon hostname'

    if sys == 'nt':
        hostname = os.getenv('computername')
    elif sys == 'posix':
        host = os.popen('echo $HOSTNAME')
        try:
            hostname = host.read()
        finally:
            host.close()
    return hostname.strip()


def get_item(lst, idx=0, trip=False):
    """
        return the first item of a list
        if trip = True, strip the item
    """
    try:
        item = lst[idx]
        if item and trip:
            item = strip_all(item)
    except IndexError:
        item = ''
    return item

def strip_all(txt):
    txt = txt.strip()
    return txt.replace("\r", '').replace("\n", '').replace(' ', '').replace("\t", '').replace(u'\xa0', '')


def strip_null(arg, null=None):
    """
        strip list,set,tuple,dict null item.

        @param:
            arg:the variable to strip null
            null:the null definition,if it is None,then use NULL as the null

        if arg is list,then strip the null item,return the new list
        if arg is tuple,then strip the null item,return the new tuple
        if arg is set,then strip the null item,return the new set
        if arg is dict,then strip the dict item which value is null.
        eturn the new dict
    """
    if null is None:
        null = NULL

    if isinstance(arg, list):
        return [i for i in arg if i not in null]
    elif isinstance(arg, tuple):
        return tuple([i for i in arg if i not in null])
    elif isinstance(arg, set):
        return arg.difference(set(null))
    elif isinstance(arg, dict):
        return {key: value for key, value in arg.items() if value not in null}

    return arg


def deduplication(arg):
    """
        deduplication the arg.

        @param:
            arg:the variable to deduplication

        if arg is list,then deduplication it and then the new list.
        if arg is tuple,then deduplication it and then the new tuple.
    """
    if isinstance(arg, list):
        return list(set(arg))
    elif isinstance(arg, tuple):
        return tuple(set(arg))
    return arg


def join_url(base_url, url, encoding):
    """
        Remove leading and trailing whitespace and punctuation
        join base url and url
    """
    url = url.decode(encoding)
    return urljoin(base_url, remove_entities(url))


def get_random_user_agent():
    """get a random user agent from a list"""
    return random.choice(USER_AGENT_LIST)


def get_exe_path(name):
    """
    找到可执行程序路径
    name: 程序名称
    return: path | None
    """
    cmd = 'which ' + name
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        return output


