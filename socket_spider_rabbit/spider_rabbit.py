import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

map_dict = {
  0: "database_spider",
  1: "local_spider",
  2: "web_spider"
}

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
    except Exception as e :
        pass
    else:
        for v in dict_map.values():
            print(v)
            result = map_dict.get(v, 0)
            if result == 0:
                spider_result = "木有该请求"
            else:
                spider_result= "我请求的是的" + str(result)
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





