# -*- coding: utf-8 -*-
import pika
import json
import time
import subprocess
from spider_spider.monitor_spider.watch_dog import FileEventHandler
from watchdog.observers import Observer

from spider_spider.search_spider.whoosh_search import chinese_analyzer

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def spider_rabbit(data):
    """
    用于执行一些耗时操作，并返回结果
    :param data:
    :return:
    """
    # 请求的json映射关系
    json_map = data.decode('utf8')
    try:
        dict_map = json.loads(json_map)
    except Exception as e:
        pass
    else:
        # 远程服务器日志获取
        if dict_map.get('num') == 0:
            p = subprocess.Popen(args='python3 ../spider_spider/ssh_log_spider/shell.py',
                                 shell=True,
                                 stdin=None,
                                 stdout=None,
                                 universal_newlines=True)
            p.wait()
            spider_result = "远程日志获取完成"
            return spider_result
        # 文件监控并发送报警邮件
        elif dict_map.get('num') == 1:
            watch_file = dict_map['watch_file']
            observer = Observer()
            event_handler = FileEventHandler()
            observer.schedule(event_handler,
                              watch_file,
                              True)
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
        # 图片采集
        elif dict_map.get('num') == 2:
            url = "http://" + dict_map['web_url']
            param = "-".join([dict_map['deep'], url])
            if dict_map.get('image_path', '') != '':
                image_store = dict_map.get('image_path', '')

            else:
                image_store = ''
            p = subprocess.Popen(args='./spider.sh {param} {image_store}'.format(param=param, image_store=image_store),
                                 shell=True,
                                 stdin=None,
                                 stdout=None,
                                 universal_newlines=True)
            p.wait()
            spider_result = "爬取完成"
            return spider_result
        # 全文检索
        elif dict_map.get('num') == 3:
            file = dict_map['file']
            key_word = dict_map['key_word']
            wh = chinese_analyzer()
            wh.create_index('/Users/chuxiaoyi/python/练习/code/毕设/design/image')
            spider_result = wh.search('褚晓逸')
            return spider_result

def on_request(ch, method, props, body):
    """
    接受客户端发来的数据，并将处理结果返回给客户端
    :param ch:
    :param method:
    :param props:
    :param body:
    :return:
    """
    response = spider_rabbit(body)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=response
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 消费者会通过一个ack（响应），告诉RabbitMQ已经收到并处理了某条消息，然后RabbitMQ就会释放并删除这条消息


channel.basic_consume(on_request, queue='rpc_queue')
print(" waiting rpc requests..... ")
channel.start_consuming()
