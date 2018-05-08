import pika
import time
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def spider_rabbit(data):
    result = "我是spider_rabbit处理过的" + data.decode('utf8')
    return result

def on_request(ch, method, props, body):
    """
    接受客户端发来的数据，并将处理结果返回给客户端
    :param ch:
    :param method:
    :param props:
    :param body:
    :return:
    """
    print(" fib(%s) "% body)
    response = spider_rabbit(body)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=response
    )

channel.basic_consume(on_request, queue='rpc_queue')
print(" waiting rpc requests..... ")
channel.start_consuming()





