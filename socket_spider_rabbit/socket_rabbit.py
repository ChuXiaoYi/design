import pika
import time

class SocketRabbit(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """
        接受消息的回调函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        self.response = body
        print(body)

    def socket_publish(self, data):
        """
        发布消息，返回的结果放在callback_queue中
        :param data:
        :return:
        """
        self.response = None
        self.corr_id = str(int(time.time()*1000))
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(data)
        )
        print("start waiting for cmd result......")
        count = 0
        while self.response is None:
            # 如果命令没有返回结果
            print("循环检查第%d次"% count)
            count+=1
            # 以不阻塞的形式去检测有没有新事件
            # 如果没有那就什么都不做，如果有，就触发on_response事件
            self.connection.process_data_events()
        return self.response


if __name__ == '__main__':
    sr = SocketRabbit()
    print(" sending cmd..... ")
    response = sr.socket_publish('chuxiaoyi')
    print(" got result! ")
    print(response.decode('utf8'))

