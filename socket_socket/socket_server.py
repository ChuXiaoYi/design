from socket import *
import sys


class Socket_Server(object):
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 8815
        self.BUFSIZE = 65535
        self.ADDR = (self.HOST, self.PORT)
        self.server_socket = None
        self.listen()

    def listen(self):
        """
        创建socket，绑定端口并监听
        :return:
        """
        try:
            self.server_socket = socket(AF_INET, SOCK_STREAM)
        except error as msg:
            print("Creating Socket Failure.Error Code: " + str(msg[0]) + "Message: " + str(msg[1]))
            sys.exit()
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置地址服用
        try:
            self.server_socket.bind(self.ADDR)
        except error as msg:
            print("Binding Failure.Error Code: " + str(msg[0]) + "Message: " + msg[1])
        self.server_socket.listen(5)

    def request_rabbit(self):
        """
        用于将处理后的客户端数据放到消息队列中
        :return:
        """
        client_server, address = self.server_socket.accept()
        print("Connected by", address)
        data = client_server.recv(self.BUFSIZE)
        client_server.sendall("我收到了！".encode('utf8'))  # 封装了send(),重复send；如果出现异常，会返回已发送的数据
        return data

    def response_rabbit(self):
        """
        用于将消息队列返回的信息发给客户端
        :return:
        """
        pass


if __name__ == '__main__':
    s = Socket_Server()
    s.request_rabbit()
