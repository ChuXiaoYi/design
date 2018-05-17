# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommonSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()R
    # 图片url
    image_urls = scrapy.Field()
    # 图片
    images = scrapy.Field()
    # 图片保存路径
    image_paths = scrapy.Field()
