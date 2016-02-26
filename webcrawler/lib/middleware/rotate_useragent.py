#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
利用随机改变useragent防止爬虫被禁止

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""


from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from webcrawler.lib.service.common import get_random_user_agent


class RotateUserAgent(UserAgentMiddleware):
    """
        a useragent middleware which rotate the user agent when crawl websites
        
        if you set the USER_AGENT_LIST in settings,the rotate with it,if not,then use the default user_agent_list attribute instead.
    """

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def _user_agent(self, spider):
        """随机获得user_agent"""
        if hasattr(spider, 'user_agent'):
            return spider.user_agent
        elif self.user_agent:
            return self.user_agent

        # return random.choice(USER_AGENT_LIST)
        return get_random_user_agent()

    def process_request(self, request, spider):
        """处理request"""
        ua = self._user_agent(spider)
        if ua:
            request.headers.setdefault('User-Agent', ua)
