import socket
import sys
import time
import select
from queue import Queue
from socket_spider_rabbit.socket_rabbit import SocketRabbit

class Socket_Server(object):
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 8888
        self.BUFSIZE = 65535
        # ip地址和端口号
        self.server_address = (self.HOST, self.PORT)
        self.server_socket = None
        self.listen()
        self.socket_rabbit = SocketRabbit()
        # self.
    def listen(self):
        """
        创建socket，绑定端口并监听
        :return:
        """
        try:
            # 创建socket对象
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print("Creating Socket Failure.Error Code: " + str(msg))
            sys.exit()
        # 设置IP地址复用
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # 绑定IP地址
            self.server_socket.bind(self.server_address)
        except Exception as msg:
            print("Binding Failure.Error Code: " + str(msg))
        # 监听，并设置最大连接数
        self.server_socket.listen(10)
        print("服务器启动成功，监听IP：", self.server_address)
        # 服务端设置非阻塞
        self.server_socket.setblocking(False)
        # 需要监听的可写入的socket
        self.inputs = [self.server_socket]
        # 处理要发送的消息的socket
        self.outputs = []
        # 要发送消息的客户端队列
        self.message_queue = {}
        # 得到回复消息的客户端队列
        self.callback_message_queue = {}

    def request_rabbit(self):
        """
        用于将处理后的客户端数据放到消息队列中
        :return:
        """
        # 处理inputs
        while self.inputs:
            print("等待下一个事件")
            # 开始select监听，对inputs列表中的服务器端server进行监听
            # 一旦调用socket的send，recv函数，将会再次调用此模块
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for s in readable:
                # 判断当前出发的是不是服务端对象，当触发的对象是服务端对象时，说明有新客户端连接进来
                # 表示有新用户来连接
                if s is self.server_socket:
                    client_socket, client_address = s.accept()
                    print('新连接，来自=>', client_address)
                    client_socket.setblocking(0)
                    # 将客户端对象也加入到监听的列表中，当客户端发送消息时select将触发
                    self.inputs.append(client_socket)
                    # 为连接的客户端单独创建一个消息队列，用来保存客户端发送的消息
                    self.message_queue[client_socket] = Queue()
                else:
                    # 有老用户发送消息，处理接受
                    # 由于客户端连接进来时服务端接受客户端连接请求，将客户端加入到了监听列表中
                    # 所以判断是否是客户端对象出发
                    data = s.recv(1024)
                    # 如果客户端未断开
                    if data != b'':
                        print('从-%s-接收到消息=>%s' % (s.getpeername(), data))
                        # 将收到的消息放入到相对应的socket客户端的消息队列中
                        self.message_queue[s].put(data)
                        # 将需要进行回复操作socket放到outputs列表中，让select监听
                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        # 客户端断开了连接，将客户端的监听从inputs列表中移除
                        print('关闭连接=>', s.getpeername())
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()
                        # 移除对应socket客户端对象的消息队列
                        del self.message_queue[s]
            # 处理outputs
            # 如果现在没有客户端请求，也没有客户端发送消息时，开始对发送消息列表进行处理，是否需要发送消息
            for s in writable:
                try:
                    # 如果消息队列中有消息，从消息队列中取出要发送的消息
                    message = self.message_queue.get(s)
                    response = ''
                    if message is not None:
                        send_data = message.get_nowait()
                        response = self.socket_rabbit.socket_publish(send_data)
                        print(response)
                except Exception as e:
                    # 客户端连接断开了
                    print("queue为空断开了连接", s.getpeername())
                    self.outputs.remove(s)
                else:
                    if message is not None:
                        print("已回复")
                        s.sendall(response)
                    else:
                        print("客户端已关闭")
            # 处理异常情况
            for s in exceptional:
                print('出现异常情况==>', s.getpeername())
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()
                del self.message_queue[s]

            time.sleep(1)



    def response_rabbit(self, body):
        """
        获取从rabbit返回的结果
        :return:
        """
        pass



if __name__ == '__main__':
    s = Socket_Server()
    s.request_rabbit()
