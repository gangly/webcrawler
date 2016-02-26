#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
test spider

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""
from .site_spider import SiteSpider

class TestSpider(SiteSpider):
    name = "test"
    # domain_name = "whatismyip.com"
    # The following url is subject to change, you can get the last updated one from here :
    # http://www.whatismyip.com/faq/automation.asp
    start_urls = [
        "http://www.baidu.com/",
        "https://www.baidu.com/s?wd=redis&pn=10",
        "https://www.baidu.com/s?wd=redis&pn=20",
        "https://www.baidu.com/s?wd=redis&pn=30"
    ]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'webcrawler.lib.middleware.ipproxy.ProxyMiddleware': 100,
        },
    }

    def parse(self, response):
        print 'ok.............%d' % response.status
