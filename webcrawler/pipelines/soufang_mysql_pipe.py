# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import logging
from webcrawler.lib.model.mysqldb import MySQL
from webcrawler.conf.pipeconf import HOUSE_ALBUM_TYPE
from webcrawler.lib.service import reg
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SoufangMysqlPipeline(object):
    """保存爬虫数据到csv文件"""
    def __init__(self):
        self.mysqldb = MySQL('light_statistics')

    def open_spider(self, spider):
        """启动spider时处理"""
        pass

    def process_item(self, item, spider):
        now = int(time.time())
        for key in item:
            if item[key] is None:
                item[key] = ''
        try:

            base_info = {
                'url': item['url'],
                'name': item['name'],
                'alias_name': item['nickname'],
                'tags': item['tags'],
                'sales_status': item['sales_status'],
                'address': item['address'],
                'avg_price': item['avgprice'],
                'open_time': item['opentime'],
                'use_time': item['launch_time'],
                'city': item['city'],
                'area': item['area'],
                'city_line': item['loop_pos'],
                'transport_address': item['traffic_cond'],
                'location_lng': item['coordx'],
                'location_lat': item['coordy'],
                'property_type': item['tenement'],
                'houses_type': item['building'],
                'property_company_name': item['property_company'],
                'property_company_address': item['property_address'],
                'property_cost': item['property_fee'],
                'property_cost_desc': item['property_add_info'],
                'green_rate': item['green_rate'],
                'plot_rate': item['volume_ratio'],
                'carport': item['parking'],
                'home_equity_year': item['period_rights'],
                'complete_time': item['completion_time'],
                'equipment': item['supporting'],
                'decoration': item['decoration'],
                'floor_area': item['area_covered'],
                'building_area': item['builtup_area'],
                'description': item['project_brief'],
                'totalrooms': item['households'],
                'sales_address': item['sale_address'],
                'developer': item['developer'],
                # 'investor': item['invest_business'],
                # 'agent': item['agent'],
                'sales_permit': item['sale_permit'],
                'status': item['progress_works'],
                'update_time': now,
                'create_time': now,
            }
            newdata = self.encode2utf8(base_info)


            self.mysqldb.insert_update('house_base_info', newdata)
            self.mysqldb.commit()

            sql = "select id from house_base_info where url = '%s'" % item['url']
            ret = self.mysqldb.query_onerow(sql)
            if ret:
                house_id = int(ret[0])
                for album_type, code in HOUSE_ALBUM_TYPE.items():
                    for key, val in item[album_type].items():
                        house_album = {
                            'house_id': house_id,
                            'album_type': code,
                            'pic_type': 'jpg',
                            'pic_title': val['title'],
                            'pic_url': val['url'],
                            'create_time': now,
                            'update_time': now,
                        }
                        house_album = self.encode2utf8(house_album)
                        self.mysqldb.insert_update('house_album', house_album)

                # ###############
                for url, val in item['img_house_type'].items():
                    type_name = val['house_type']
                    if not type_name:
                        continue
                    type_num = reg.find_all_int(type_name)
                    try:
                        room = type_num[0]
                    except IndexError:
                        room = 0
                    try:
                        hall = type_num[1]
                    except IndexError:
                        hall = 0
                    try:
                        kitchen = type_num[2]
                    except IndexError:
                        kitchen = 0
                    try:
                        toilet = type_num[3]
                    except IndexError:
                        toilet = 0
                    house_type = {
                        'house_id': house_id,
                        'house_type_name': type_name,
                        'house_type_room': room,
                        'house_type_hall': hall,
                        'house_type_kitchen': kitchen,
                        'house_type_toilet': toilet,
                        'house_area': val['area'],
                        'house_price_avg': val['avg'],
                        'house_price_sum': val['total'],
                        'pic_url': val['url'],
                        'create_time': now,
                        'update_time': now,
                    }
                    house_type = self.encode2utf8(house_type)
                    self.mysqldb.insert_update('house_type', house_type)


            self.mysqldb.commit()

        except Exception as e:
            logging.error("db error: %s" % e)
        return item

    def close_spider(self, spider):
        """关闭spider时动作"""
        self.mysqldb.close()

    def encode2utf8(self, data):
        newdata = {}
        for key, val in data.items():
            if isinstance(val, unicode):
                newdata[key] = val.encode('utf8')
            else:
                newdata[key] = val
        return newdata


