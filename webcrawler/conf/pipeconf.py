#!/usr/bin/env python 2.7
# -*- coding:utf-8 -*-
'''
     有关pipeline的配置
'''
from webcrawler.lib.service import common 
host = common.gethostname()

IMG_HOST_PATH = 'http://%s:8081/image/' % host

HOUSE_ALBUM_TYPE = {
    'img_effect': 1,
    'img_scene': 2,
    'img_traffic': 3,
    'img_mating': 4,
}
