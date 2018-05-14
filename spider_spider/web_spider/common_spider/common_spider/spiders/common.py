# -*- coding: utf-8 -*-
import scrapy
import sys

from common_spider.items import CommonSpiderItem


class CommonSpider(scrapy.Spider):
    name = 'common'

    def __init__(self, target="1-www.baidu.com"):
        super(CommonSpider, self).__init__(target=target)
        # 爬取深度
        self.deep_num = target.split("-")[0]
        self.start_urls = [target.split("-")[1]]
        self.allowed_domains = [target.split("-")[1].split(".", 1)[1].split('/')[0]]


    def parse(self, response):
        # 页面全部图片链接
        imgs = response.xpath('//img[contains(@src, ".jpg")]/@src').extract()
        # 页面全部url
        all_url = response.xpath('//body//a[contains(@href, "http")]/@href').extract()
        if imgs != []:
            for img in imgs:
                item = CommonSpiderItem()
                item['img_url'] = img
                item['url'] = response.request._url
                yield item
        else:
            item = CommonSpiderItem()
            item['img_url'] = ""
            item['url'] = response.request._url
            yield item
        print(response.request.meta['depth'])
        if response.request.meta['depth']+1 < int(self.deep_num):
            print(self.deep_num)
            for url in all_url:
                if url.find(r'.com') > 0 or url.find(r'.cn') > 0:
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse)



