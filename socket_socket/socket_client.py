from socket import *

'''配置信息'''
HOST = '127.0.0.1'
PORT = 8812
BUFSIZE = 65535 # 设置缓冲区大小
ADDR = (HOST, PORT)

'''创建socket，建立连接'''
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8815))

while True:
    data = input("输入：")
    client_socket.sendall(data.encode('utf8'))
    rsv_data = client_socket.recv(BUFSIZE)
    print(rsv_data.decode('utf8'))
client_socket.close()
