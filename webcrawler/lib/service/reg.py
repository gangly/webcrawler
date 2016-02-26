#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
对正则表达式函数的封装

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""
import re

def find_float(data):
    patt = re.compile(r"(\d+[\.\d]\d+)")
    ret = patt.findall(data)
    return float(ret[0]) if ret else 0

def find_int(data):
    patt = re.compile(r"(\d+)")
    ret = patt.findall(data)
    return int(ret[0]) if ret else 0

def find_all_int(data):
    patt = re.compile(r"(\d+)")
    ret = patt.findall(data)
    return [int(dd) for dd in ret]