import pika


class SpiderRabbit(object):
    def __init__(self, host):
        self.host = host
        self.util_data = dict()  # 用于存储当前对象内的所有工具字段
        self.connect_rabbit()

    def connect_rabbit(self):
        """
        建立一个到RabbitMQ服务器的连接
        :return:
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        self.util_data['connection'] = connection  # 工具字段——connection,channel
        self.util_data['channel'] = channel  # 工具字段——channel

    def spider_cusuming(self):
        """
        用于处理回调队列的内容
        :return:
        """
        channel = self.util_data['channel']
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.__on_response, no_ack=False, queue='rpc_queue')
        channel.start_consuming()

    def __on_response(self, ch, method, props, body):
        """
        回调函数
        作用是处理远程操作，并将结果发布给socket
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 消费者会通过一个ack（响应），告诉RabbitMQ已经收到并处理了某条消息，然后RabbitMQ就会释放并删除这条消息
        print(body.decode('utf8'))
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body="我是处理过的{body}".format(body=body.encode('utf8'))
        )


if __name__ == '__main__':
    host = 'localhost'
    sr = SpiderRabbit(host)
    sr.spider_cusuming()


