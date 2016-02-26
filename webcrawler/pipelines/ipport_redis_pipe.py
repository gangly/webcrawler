# -*- coding: utf-8 -*-

from webcrawler.conf import redisconf
from webcrawler.lib.model.redisdb import get_redis_server


class IpportRedisPipe(object):
    """保存爬虫数据到csv文件"""
    def __init__(self):
        self.rdb = get_redis_server()

    def process_item(self, item, spider):
        ipports = item['ipport']
        for ipport in ipports:
            if self.rdb.scard('ipport') > redisconf.IPPORT_MAX:
                break
            self.rdb.sadd('ipport', ipport)

    def close_spider(self, spider):
        """关闭spider时动作"""
        # self.rdb.shutdown()
