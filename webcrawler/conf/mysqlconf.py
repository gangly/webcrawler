#!/usr/bin/env python 2.7
# -*- coding:utf-8 -*-
'''
     * 数据库库名与集群编号的映射关系表，说明每个数据库部署在哪个集群上
     * 每增加一个数据库时必须在这里增加一个映射记录，如果不增加映射记录，
     * 则默认认为该数据库部署在第一个集群上
     * @var array
'''
DB_NAMES = {
    # 本地xampp测试库
    'local_test': {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'root',
        'db': 'test',
        'charset': 'utf8'
    },
    # hummer测试库地址
    'light_statistics': {
        'host': '10.208.162.20',
        'port': 3306,
        'user': 'light_dev',
        'passwd': 'lightgogo',
        'db': 'light_statistics',
        'charset': 'utf8'
    },
    # hummer线上库地址
    'lightapp_hummer': {
        'host': '10.202.6.141',
        'port': 7046,
        'user': 'la_hummer_w',
        'passwd': 'MsOZPcI4zUhh1k1c',
        'db': 'lightapp_hummer',
        'charset': 'utf8'
    },
    # hummer线上库备库
    'lightapp_hummer_pre': {
        'host': 'sh01-dba-chunlei-hummer-03.sh01',
        'port': 5108,
        'user': 'la_hummer_w',
        'passwd': 'MsOZPcI4zUhh1k1c',
        'db': 'lightapp_hummer',
        'charset': 'utf8'
    },
    # hummer线上PALO库地址
    'hummer_palo_dev': {
        'host': '10.202.95.41',
        'port': 9420,
        'user': 'hummer_dev',
        'passwd': 'hummergogo',
        'db': 'hummer_palo_dev',
        'charset': 'utf8'
    },
    # 开发者中心库
    'mco_developer_openplatform': {
        'host': '10.202.95.49',
        'port': 5352,
        'user': 'openplatform_r',
        'passwd': 'oY3DHhmW1BFfkUYy',
        'db': 'mco_developer_openplatform',
        'charset': 'utf8'
    },
}


# 连接重试次数及间隔时间
TRY_LINK_COUNT = 2
INTERVAL_TIME_SECOND = 5
