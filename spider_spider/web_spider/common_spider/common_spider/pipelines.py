# -*- coding: utf-8 -*-
import json
from scrapy.contrib.pipeline.images import ImagesPipeline,DropItem
import scrapy


class CommonSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """
        对图片url进行下载
        :param item:
        :param info:
        :return:
        """
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("没有图片")
        item['image_paths'] = image_paths
        return item
