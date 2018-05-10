import socket
import time
import json

def main(num):
    server_address = ('127.0.0.1', 8888)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("正在连接%s，端口号为%s" % server_address)
    client_socket.connect(server_address)
    data = json.dumps({
            client_socket.getsockname()[1]: int(num)
        }, ensure_ascii=False)
    client_socket.sendall(data.encode('utf8'))
    result = client_socket.recv(65535)
    print("%s received %s" % (client_socket.getsockname(), result.decode('utf8')))
    if data != "":
        print('closeingsocket', client_socket.getsockname())
        time.sleep(1)
        client_socket.close()


if __name__ == '__main__':
    while True:
        num = input("输入你想请求的spider：")
        main(num)