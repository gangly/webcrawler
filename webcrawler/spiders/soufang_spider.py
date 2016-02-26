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
import time
import json
import requests
import logging
from scrapy.http import Request
from .site_spider import SiteSpider
from scrapy.conf import settings
from webcrawler.lib.service import log
# from scrapy.conf import settings
from webcrawler.items.soufang_item import SoufangItem
from webcrawler.lib.service import common
from webcrawler.lib.service import reg
# from webcrawler.lib.service.common import join_url


class SoufangSpider(SiteSpider):
    """定向搜房网信息"""
    name = "soufang"

    start_urls = (
        # u'http://newhouse.tj.fang.com/house/s/b81-b91/',
        u'http://newhouse.tj.fang.com/house/s/b82-b91/',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'webcrawler.pipelines.soufang_image_pipe.SoufangImageEffect': 1,
            'webcrawler.pipelines.soufang_image_pipe.SoufangImageScene': 2,
            'webcrawler.pipelines.soufang_image_pipe.SoufangImageTraffic': 3,
            'webcrawler.pipelines.soufang_image_pipe.SoufangImageMating': 4,
            'webcrawler.pipelines.soufang_image_pipe.SoufangImageHouseType': 5,
            'webcrawler.pipelines.soufang_mysql_pipe.SoufangMysqlPipeline': 6,
        },
    }

    # allowed_domains = ["s.lvmama.com", "ticket.lvmama.com"]
    # ITEM_PIPELINES = {
    #     # 'scrapy_redis.pipelines.RedisPipeline': 1,
    #     'webcrawler.pipelines.TestPipeline': 300,
    # }
    # settings.set('ITEM_PIPELINES', ITEM_PIPELINES)
    # 
    def __init__(self):
        log.init_log(settings.get('LOG_DIR'))
        logging.info("spider start......")
        print "spider start......"
        logging.error(settings.get('LOG_DIR'))


    def parse(self, response):
        """解析网页"""

        path = u"//a[@class='next']/@href"
        next_link = self.get_elem(response, path)
        
        time.sleep(2)
        if next_link:
            next_link = common.join_url(response.url, next_link, response.encoding)
            yield Request(url=next_link, callback=self.parse)

        path = u"//div[@class='nlcd_name']/a[1]/@href"
        for detail_link in response.xpath(path).extract():
            yield Request(url=detail_link, callback=self.parse_item)

    def parse_item(self, response):
        """parse the detail url"""
        item = SoufangItem()

        item['sales_status'] = 2 #    1
        item['url'] = response.url

        path = "//a[@class='ts_linear']/text()"
        item['name'] = self.get_elem(response, path)

        path = "//span[@class='h1_label']/text()"
        item['nickname'] = self.get_elem(response, path)

        path = "//div[@class='lpicon tf']/node()/node()/text()"
        item['tags'] = self.get_nodes_text(response, path)
        if not item['tags']:
            path = "//div[@class='lpicon tf']/node()/text()"
            item['tags'] = self.get_nodes_text(response, path)

        path = "//span[@class='prib cn_ff']/text()"
        item['avgprice'] = self.get_int(response, path)

        path = "//div[@class='information_li'][4]/div/p/a/text()"
        item['opentime'] = self.get_elem(response, path)

        path = "//div[@class='information_li'][5]/div/p/span/text()"
        item['address'] = self.get_elem(response, path)

        path = "//div[@class='br_left']/div/ul/li[2]/a/text()"
        data = self.get_elem(response, path)
        item['city'] = data.replace(u'新房', '')

        path = "//div[@class='br_left']/div/ul/li[3]/a/text()"
        data = self.get_elem(response, path)
        item['area'] = data.replace(u'楼盘', '')

        # 楼盘坐标
        path = "//meta[@name='location']/@content"
        data = self.get_elem(response, path)
        try:
            # city=\u5929\u6d25;coord=117.07233428955078000000,39.39088439941406000000;
            data = data.split(';')[1]
            data = data.replace('coord=', '')
            coord = data.split(',')
            item['coordx'] = float(coord[0])
            item['coordy'] = float(coord[1])
        except IndexError:
            pass


        # 楼盘详情链接
        path = u"//div[@id='orginalNaviBox']//a[text()='楼盘详情']/@href"
        housedetail_link = self.get_elem(response, path)
        yield Request(url=housedetail_link, meta={'item': item}, callback=self.parse_housedetail)

        

    def parse_housedetail(self, response):
        """
        楼盘详情
        """
        item = response.meta['item']

        path = "//div[@class='besic_inform']/table//text()"
        elems = response.xpath(path).extract()
        elems = [common.strip_all(elem) for elem in elems]
       
        for idx, elem in enumerate(elems):
            if elem.find(u'物业类别') >= 0:
                item['tenement'] = elems[idx+1]
            elif elem.find(u'建筑类别') >= 0:
                item['building'] = elems[idx+1]
            elif elem.find(u'环线位置') >= 0:
                try:
                    item['loop_pos'] = elems[idx+2]
                except IndexError as e:
                    logging.error("IndexError: %s" % e)
            elif elem.find(u'建筑类别') >= 0:
                item['building'] = elems[idx+1]
            elif elem == u'容积率':
                item['volume_ratio'] = reg.find_float(elems[idx+1])
            elif elem.find(u'物业费') >= 0:
                item['property_fee'] = elems[idx+1]
            elif elem.find(u'开发商') >= 0:
                item['developer'] = elems[idx+1]
            elif elem == u'预售许可证':
                item['sale_permit'] = elems[idx+1]
            elif elem.find(u'售楼地址') >= 0:
                item['sale_address'] = elems[idx+1]
            elif elem.find(u'物业地址') >= 0:
                item['property_address'] = elems[idx+1]
            elif elem.find(u'交通状况') >= 0:
                item['traffic'] = elems[idx+1]
            elif elem.find(u'项目特色') >= 0:
                item['project_character'] = elems[idx+1]
            elif elem.find(u'装修状况') >= 0:
                item['decoration'] = elems[idx+1]
            elif elem.find(u'装修案例') >= 0:
                item['decoration_case'] = elems[idx+1]
            elif elem == u'绿化率':
                item['green_rate'] = reg.find_int(elems[idx+1])
            elif elem == (u'交房时间'):
                item['launch_time'] = elems[idx+1]
            elif elem.find(u'物业公司') >= 0:
                item['property_company'] = elems[idx+1]
        

        ##############
        
       # 项目配套
        path = "//div[@class='besic_inform']/div[@class='lineheight'][2]/text()"
        item['supporting'] = self.get_elem(response, path) 

        # 交通状况
        path = "//div[@class='besic_inform']/div[@class='lineheight'][3]/text()"
        item['traffic_cond'] = self.get_elem(response, path) 

        # 车位信息
        path = "//div[@class='besic_inform']/div[@class='lineheight'][6]/text()"
        item['parking'] = self.get_elem(response, path)

        # 项目简介
        path = "//div[@class='besic_inform']/div[@class='lineheight'][7]/text()"
        item['project_brief'] = self.get_elem(response, path)

        # related_info # 相关信息
        path = "//div[@class='besic_inform']/div[@class='lineheight'][8]//text()"

        elems = response.xpath(path).extract()
        elems = [common.strip_all(elem) for elem in elems]
        # print elems
        for idx, elem in enumerate(elems):
            if elem.find(u'占地面积:') >= 0:
                item['area_covered'] = reg.find_int(elems[idx+1])
            elif elem.find(u'建筑面积:') >= 0:
                item['builtup_area'] = reg.find_int(elems[idx+1])
            elif elem.find(u'开工时间:') >= 0:
                item['onstream_time'] = elems[idx+1]
            elif elem.find(u'竣工时间:') >= 0:
                item['completion_time'] = elems[idx+1]
            elif elem.find(u'物业管理附加信息:') >= 0:
                item['property_add_info'] = elems[idx+1]
            elif elem.find(u'开发商:') >= 0:
                item['developer'] = elems[idx+1]
            elif elem.find(u'物业管理公司:') >= 0:
                item['property_company'] = elems[idx+1]
            elif elem.find(u'按揭银行:') >= 0:
                item['mortgage_bank'] = elems[idx+1]
            elif elem.find(u'工程进度:') >= 0:
                item['progress_works'] = elems[idx+1]
            elif elem.find(u'产权年限:') >= 0:
                item['period_rights'] = elems[idx+1]
            elif elem.find(u'户数:') >= 0:
                item['households'] = reg.find_int(elems[idx+1])

        # 楼盘相册链接
        path = u"//div[@id='orginalNaviBox']//a[text()='楼盘相册']/@href"
        image_link = self.get_elem(response, path)
        yield Request(url=image_link, meta={'item': item}, callback=self.parse_image)

    def parse_image(self, response):

        item = response.meta['item']
        path = "//div[@class='xc_xmdl clearfix']/dl[@class='dl']//a/@href"
        links = response.xpath(path).extract()

        meta = {
            'item': item,
            'next': 0,
            'links': links,
        }
        if not links:
            yield item
        else:
            newlinks = []
            img_house_type_link = ''
            for link in links:
                if not link.startswith('http://'):
                    link = common.join_url(response.url, link, response.encoding)
                if link.find('list_900_') >= 0:
                    img_house_type_link = link
                else:
                    newlinks.append(link)
            meta['links'] = newlinks
            meta['img_house_type_link'] = img_house_type_link
            item['img_house_type'] = {}
            if newlinks:
                yield Request(url=newlinks[0], meta=meta, callback=self.parse_image_effect)
            else:
                yield Request(url=img_house_type_link, meta=meta, callback=self.parse_img_house_type)


    def parse_image_effect(self, response):

        time.sleep(1)

        meta = response.meta
        item = meta['item']
        

        typedic = {
            '904': 'img_effect',        # 效果图
            '903': 'img_scene',         # 实景图
            '901': 'img_traffic',           # 交通图
            '907': 'img_mating',    # 配套图
            # '900': 'img_house_type',  # 户型图
            # '1003': 'img_decorate',     # 装修案例
        }

        url = response.url

        # http://haiheyuanzhu.fang.com/photo/list_907_1110769899.htm
        # http://haiheyuanzhu.fang.com/house/ajaxrequest/photolist_get.php?newcode=1110769899&type=907&nextpage=2&room=
        # 
        elems = url.split('/photo/')
        host = elems[0]
        para1 = elems[1].split('.')[0]
        para2 = para1.split('_')
        ptype = para2[1]
        pnewcode = para2[2]
        args = (host, pnewcode, ptype)
        new_url = "%s/house/ajaxrequest/photolist_get.php?newcode=%s&type=%s&nextpage=" % args

        
        if ptype in typedic:
            nextpage = 1
            simg = {}
            while True:
                real_url = new_url + str(nextpage)
                ret = requests.get(real_url)
                if ret.status_code != 200:
                    break
                data = json.loads(ret.content)
                if isinstance(data, list):
                    for dat in data:
                        info = {}
                        info['title'] = dat['title']
                        simg[dat['url']] = info
                else:
                    break
                nextpage += 1
            
            item[typedic[ptype]] = simg

        # meta = response.meta
        meta['item'] = item
        meta['next'] = meta['next']+1
        nxt = meta['next']
        links = meta['links']
        
        if nxt >= len(meta['links']):
            link = meta['img_house_type_link']
            if link:
                yield Request(url=link, meta=meta, callback=self.parse_img_house_type)
            else:
                yield item
        else:
            yield Request(url=links[nxt], meta=meta, callback=self.parse_image_effect)



    def parse_img_house_type(self, response):

        meta = response.meta
        item = meta['item']

        path = "//div[@class='big_img']/a/img/@src"
        img_url = self.get_elem(response, path)

        path = "//div[@class='lp_xinxi fl']/ul/li//text()"
        elems = response.xpath(path).extract()
        elems = [common.strip_all(elem) for elem in elems]
        info = {}
        # print elems
        for idx, elem in enumerate(elems):
            if elem.find(u'居室') >= 0:
                info['house_type'] = elems[idx+1]
            elif elem.find(u'户型分布') >= 0:
                info['spread'] = elems[idx+1]
            elif elem.find(u'建筑面积') >= 0:
                info['area'] = reg.find_int(elems[idx+1])
            elif elem.find(u'参考均价') >= 0:
                info['avg'] = reg.find_int(elems[idx+1])
            elif elem.find(u'参考总价') >= 0:
                info['total'] = reg.find_int(elems[idx+1])
        # info['img_url'] = img_url

        if img_url:
            item['img_house_type'][img_url] = info


        path = "//div[@class='big_img']/a[@class=' big_btn big_img_next']/@href"
        link = self.get_elem(response, path)
        meta['item'] = item
        if link:
            yield Request(url=link, meta=meta, callback=self.parse_img_house_type)
        else:
            yield item


