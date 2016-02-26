#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2015 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
定向抓取信息

Authors: Gary(ligang05@baidu.com)
Date:    2015/07/07 17:23:06
"""
# import re
# import json
# import requests

import logging
import time
from scrapy.http import Request
from .site_spider import SiteSpider
# from scrapy.conf import settings
from webcrawler.items.ipproxy_item import IpproxyItem


class IpportSpider(SiteSpider):
    """crawl ips from webs"""
    name = "ipport"

    custom_settings = {
        'ITEM_PIPELINES': {
            'webcrawler.pipelines.ipport_redis_pipe.IpportRedisPipe': 1,
        },
    }

    def start_requests(self):
        start_reqs = [
            Request(url='http://www.xicidaili.com/nn/1', callback=self.parse_xicidaili),
            Request(url='http://www.kuaidaili.com/free/', callback=self.parse_kuaidaili),

        ]
        return start_reqs


    def parse_xicidaili(self, response):
        """解析网页"""
        item = IpproxyItem()

        ips = response.xpath("//table[@id='ip_list']/tr/td[3]/text()").extract()
        ports = response.xpath("//table[@id='ip_list']/tr/td[4]/text()").extract()
        item['ipport'] = self.make_ppport_list(ips, ports)
        print 'haha..............in parse!'

        yield item

    def parse_kuaidaili(self, response):
        item = IpproxyItem()

        ips = response.xpath("//div[@id='list']/table/tbody/tr/td[1]/text()").extract()
        ports = response.xpath("//div[@id='list']/table/tbody/tr/td[2]/text()").extract()
        item['ipport'] = self.make_ppport_list(ips, ports)
        print 'haha..............in parse!'

        yield item

    def make_ppport_list(self, ips, ports):

        time.sleep(4)
        sz = len(ips)
        if sz != len(ports):
            logging.error("the length of ips and ports lists are not equel.")
            exit(1)
        i = 0
        ipportlist = []
        while(i < sz):
            ipport = ips[i] + ":" + ports[i]
            ipportlist.append(ipport)
            i += 1

        return ipportlist
