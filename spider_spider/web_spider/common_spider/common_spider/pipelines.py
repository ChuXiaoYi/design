# -*- coding: utf-8 -*-
import json
from scrapy.contrib.pipeline.images import ImagesPipeline, DropItem

import scrapy


class CommonSpiderPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        """
        改写文件名称
        :param request:
        :param response:
        :param info:
        :return:
        """
        image_guid = request.url.split('/')[-1]
        return 'web_image/%s' % (image_guid)

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
