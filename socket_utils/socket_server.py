# -*-coding=utf-8-*-
# !/usr/bin/python
from socket import *
import sys

'''配置信息'''
HOST = '127.0.0.1'
PORT = 8815
BUFSIZE = 65535
ADDR = (HOST, PORT)

'''创建socket，绑定端口并监听'''
try:
    server_socket = socket(AF_INET, SOCK_STREAM)
except error, msg:
    print "Creating Socket Failure.Error Code: " + str(msg[0]) + "Message: " + str(msg[1])
    sys.exit()
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置地址服用
try:
    server_socket.bind(ADDR)
except error, msg:
    print "Binding Failure.Error Code: " + str(msg[0]) + "Message: " + msg[1]
server_socket.listen(5)

while True:
    '''获取客户端和地址'''
    client_server, address = server_socket.accept()
    print "Connected by", address
    while True:
        data = client_server.recv(BUFSIZE)
        print data
        # This calls send() repeatedly until all data is sent.
        # If an error occurs,it's impossible to tell how much data has been sent.
        client_server.sendall("我收到了！")
server_socket.close()
