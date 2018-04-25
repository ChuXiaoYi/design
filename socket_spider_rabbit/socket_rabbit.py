import pika
import time


class SocketRabbit(object):
    def __init__(self, host_name):
        self.host = host_name
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

    def socket_publish(self):
        """
        用于发布任务，并设置回调队列
        也是外部调用接口
        :return:
        """
        result = self.util_data['channel'].queue_declare(exclusive=True)  # exclusive:当与消费者断开连接的时候，这个队列应当被立即删除
        callback_queue = result.method.queue
        correlation_id = str(int(time.time() * 1000))
        self.util_data['channel'].basic_publish(exchange='',
                                                routing_key='rpc_queue',
                                                properties=pika.BasicProperties(
                                                    reply_to=callback_queue,
                                                    correlation_id=correlation_id),
                                                body=str(1))
        self.util_data['callback_queue'] = callback_queue  # 工具字段——callback_queue——回调队列
        self.util_data['correlation_id'] = correlation_id  # 工具字段——correlation_id——用于和返回的correlation_id比较
        self.socket_cusuming()

    def socket_cusuming(self):
        """
        用于处理回调队列的内容
        :return:
        """
        channel = self.util_data['channel']
        channel.basic_consume(self.__on_response, no_ack=True, queue=self.util_data['callback_queue'])
        channel.start_consuming()

    def __on_response(self, ch, method, props, body):
        """
        回调队列对应的custom的回调函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if props.correlation_id == self.util_data['correlation_id']:
            print(body.decode('utf8'))


if __name__ == '__main__':
    host = 'localhost'
    sr = SocketRabbit(host)
    sr.socket_publish()
