#!/usr/bin/python
#-*-coding:utf-8-*-

import os
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from webcrawler.conf.pipeconf import IMG_HOST_PATH


class SoufangImageEffect(ImagesPipeline):
    """
        this is for download the book covor image and then complete the 
        book_covor_image_path field to the picture's path in the file system.
    """

    def get_media_requests(self, item, info):
        if item.get('img_effect'):
            for image_url in item['img_effect']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        # image_paths = [x['path'] for ok, x in results if ok]
        # item['img_effect_path'] = image_paths
        # print item
        for ok, x in results:
            if ok:
                item['img_effect'][x['url']]['url'] = IMG_HOST_PATH+x['path']
        return item


class SoufangImageScene(ImagesPipeline):
    """
        this is for download the book covor image and then complete the 
        book_covor_image_path field to the picture's path in the file system.
    """

    def get_media_requests(self, item, info):
        if item.get('img_scene'):
            for image_url in item['img_scene']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                item['img_scene'][x['url']]['url'] = IMG_HOST_PATH+x['path']
        return item


class SoufangImageTraffic(ImagesPipeline):
    """
        this is for download the book covor image and then complete the 
        book_covor_image_path field to the picture's path in the file system.
    """

    def get_media_requests(self, item, info):
        if item.get('img_traffic'):
            for image_url in item['img_traffic']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                item['img_traffic'][x['url']]['url'] = IMG_HOST_PATH+x['path']
        return item


class SoufangImageMating(ImagesPipeline):
    """
        this is for download the book covor image and then complete the 
        book_covor_image_path field to the picture's path in the file system.
    """

    def get_media_requests(self, item, info):
        if item.get('img_mating'):
            for image_url in item['img_mating']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                item['img_mating'][x['url']]['url'] = IMG_HOST_PATH+x['path']
        return item


class SoufangImageHouseType(ImagesPipeline):
    """
        this is for download the book covor image and then complete the 
        book_covor_image_path field to the picture's path in the file system.
    """
    def get_media_requests(self, item, info):
        if item.get('img_house_type'):
            for image_url in item['img_house_type']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                item['img_house_type'][x['url']]['url'] = IMG_HOST_PATH+x['path']
        return item
