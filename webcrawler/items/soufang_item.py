# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoufangItem(scrapy.Item):
    sales_status = scrapy.Field(default=0)   # 销售状态 1:在售
    url = scrapy.Field(default='')       # 房产地址
    name = scrapy.Field(default='')       # 房产名
    nickname = scrapy.Field(default='')   # 房产别名
    tags = scrapy.Field(default='')       # 标签
    avgprice = scrapy.Field(default=0)   # 平均价格
    opentime = scrapy.Field(default='')   # 最新开盘
    address = scrapy.Field(default='')    # 楼盘地址

    city = scrapy.Field(default='')       # 城市
    area = scrapy.Field(default='')       # 行政区域
    coordx = scrapy.Field(default=0)     # x坐标
    coordy = scrapy.Field(default=0)     # y坐标

    # house detail
    tenement = scrapy.Field(default='')       # 物业类别
    building = scrapy.Field(default='')       # 建筑类别
    loop_pos = scrapy.Field(default='')        # 环线位置
    volume_ratio = scrapy.Field(default=0)       # 容 积 率
    property_fee = scrapy.Field(default='')   # 物 业 费
    developer = scrapy.Field(default='')      # 开 发 商
    sale_permit = scrapy.Field(default='')    # 预售许可证
    sale_address = scrapy.Field(default='')   # 售楼地址
    property_address = scrapy.Field(default='')   # 物业地址
    traffic = scrapy.Field(default='')            # 交通状况
    project_character = scrapy.Field(default='')  # 项目特色
    decoration = scrapy.Field(default='')         # 装修状况
    decoration_case = scrapy.Field(default='')  # 装修案例
    green_rate = scrapy.Field()         # 绿 化 率
    launch_time = scrapy.Field(default='')        # 交房时间
    property_company = scrapy.Field(default='')   # 物业公司

    # ###
    supporting = scrapy.Field(default='')     # 项目配套
    traffic_cond = scrapy.Field(default='')   # 交通状况
    parking = scrapy.Field(default='')    # 车位信息
    project_brief = scrapy.Field(default='')  # 项目简介
    # related_info # 相关信息
    area_covered = scrapy.Field(default=0)   # 占地面积

    builtup_area = scrapy.Field(default=0)   # 建筑面积
    onstream_time = scrapy.Field(default='')  # 开工时间
    completion_time = scrapy.Field(default='')    # 竣工时间
    property_add_info = scrapy.Field(default='')  # 物业管理附加信息
    # Developers # 开发商
    invest_business = scrapy.Field(default='')    # 投资商
    # Property Management Company # 物业管理公司
    agent = scrapy.Field(default='')  # 代理商
    mortgage_bank = scrapy.Field(default='')  # 按揭银行
    progress_works = scrapy.Field(default='')     # 工程进度
    period_rights = scrapy.Field(default=0)  # 产权年限
    households = scrapy.Field(default=0)     # 户 数

    # 图片
    # image_urls = scrapy.Field()
    # images = scrapy.Field()

    img_effect = scrapy.Field()        # 效果图
    img_scene = scrapy.Field()         # 实景图
    img_traffic = scrapy.Field()           # 交通图
    img_mating = scrapy.Field()     # 配套图
    img_house_type = scrapy.Field()     # 户型图
    img_decorate = scrapy.Field()     # 装修案例

    # img_effect_path = scrapy.Field()        # 效果图
    # img_scene_path = scrapy.Field()         # 实景图
    # img_traffic_path = scrapy.Field()           # 交通图
    # img_mating_path = scrapy.Field()     # 配套图
    # img_house_type_path = scrapy.Field()     # 户型图
    # img_decorate_path = scrapy.Field()     # 装修案例
