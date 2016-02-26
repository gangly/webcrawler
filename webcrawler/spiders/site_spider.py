#!/usr/bin/env python 2.7
# -*-coding:UTF-8-*-
"""爬虫基类"""
import os
import csv
import scrapy
from scrapy.spiders import Spider

from webcrawler.lib.service import common
from webcrawler.lib.service import log
from webcrawler.lib.service import reg
from scrapy.conf import settings


class SiteSpider(Spider):
    """爬虫基类"""

    def __init__(self):
        log.init_log(settings.get('LOG_DIR'))

    def parse(self, response):
        """BaseSpider parse"""
        pass

    def get_int(self, response, path, idx=0, trip=True):
        data = self.get_elem(response, path, idx, False)
        return reg.find_int(data)

    def get_float():
        data = self.get_elem(response, path, idx, False)
        return reg.find_float(data)

    def get_elem(self, response, path, idx=0, trip=True):
        """
            根据xpath返回的是一个list
        """
        lst = response.xpath(path).extract()
        return common.get_item(lst, idx, trip)

    def get_all_text(self, response, path, trip=True):
        """
            获取xpath下所有文字
        """
        xpth = response.xpath(path)
        text_lst = xpth.xpath('string(.)').extract()
        return common.get_item(text_lst, 0, trip)

    def get_nodes_text(self, response, path, spliter=',', trip=True):
        """
            获取某级子节点下的文字,数据返回一个列表
        """
        data = response.xpath(path).extract()
        txt = spliter.join(data)
        if trip:
            txt = common.strip_all(txt)
        return txt


    def save2csv(self, file_name, items):
        """
        保存数据到文件
        默认为csv格式
        """
        writer = csv.writer(open(file_name), 'wb')
        writer.writerows(items)
