# -*- coding: utf-8 -*-
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CommonSpiderPipeline(object):
    def __init__(self):
        self.result_list = list()

    def process_item(self, item, spider):
        self.result_list.append({
            "url": item['url'],
            "img_url": item['img_url']
        })
        with open('./result.json', 'w') as f:
            f.write(json.dumps(self.result_list, ensure_ascii=False))
        return item
