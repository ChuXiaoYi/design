#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 下午2:21
# @Author  : cxy
# @Site    : 
# @File    : whoosh_search.py
# @Software: PyCharm
# @desc    :

import jieba
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import RegexAnalyzer
from whoosh.analysis import Tokenizer, Token


class ChineseTokenizer(Tokenizer):
    """
    中文分词解析器
    """

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=True, removestops=True, start_pos=0, start_char=0,
                 mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode " % value
        t = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
        list_seg = jieba.cut_for_search(value)
        for w in list_seg:
            t.original = t.text = w
            t.boost = 0.5
            if positions:
                t.pos = start_pos + value.find(w)
            if chars:
                t.startchar = start_char + value.find(w)
                t.endchar = start_char + value.find(w) + len(w)
            yield t

    @staticmethod
    def create_index(document_dir):
        """
        构建索引
        :param document_dir:
        :return:
        """
        analyzer = chinese_analyzer()
        schema = Schema(titel=TEXT(stored=True, analyzer=analyzer), path=ID(stored=True),
                        content=TEXT(stored=True, analyzer=analyzer))
        ix = create_in("/Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/search_spider/schema", schema)
        writer = ix.writer()
        for parents, dirnames, filenames in os.walk(document_dir):
            for filename in filenames:
                title = filename.replace(".txt", "")
                print("文件名：{title}".format(title=title))
                content = open(os.path.join(document_dir, filename), 'r', encoding='utf8').read()
                path = u"/Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/search_spider/schema"
                writer.add_document(titel=title, path=path, content=content)
        writer.commit()

    @staticmethod
    def search(search_str):
        """
        关键词搜索
        :param search_str:
        :return:
        """
        result_list = []
        print('开始查找。。。。。')
        ix = open_dir("/Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/search_spider/schema")
        searcher = ix.searcher()
        print("正在检索：{search_str}".format(search_str=search_str))
        results = searcher.find("content", search_str)
        for hit in results:
            # 文件名
            file_name = hit['titel']
            # 内容
            content = hit.highlights("content", top=100, minscore=5)
            result_list.append((file_name, content))
        return result_list


def chinese_analyzer():
    return ChineseTokenizer()


if __name__ == '__main__':
    wh = chinese_analyzer()
    wh.create_index('/Users/chuxiaoyi/python/练习/code/毕设/design/image')
    print(wh.search('褚晓逸'))
