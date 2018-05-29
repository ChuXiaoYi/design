#!/bin/bash
cd /Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/web_spider/common_spider
/Library/Frameworks/Python.framework/Versions/3.6/bin/scrapy crawl common -a target="$1" -s IMAGES_STORE="$2"
