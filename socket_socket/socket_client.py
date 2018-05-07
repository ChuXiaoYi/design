import socket
import time
messages = ["a", "b", "c"]
server_address = ('127.0.0.1', 8815)
client_sockets = [
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
]
print("正在连接%s，端口号为%s"% server_address)
# 连接到服务器
for c_s in client_sockets:
    c_s.connect(server_address)

for index, message in enumerate(messages):
    for c_s in client_sockets:
        print("%s: sending %s"% (c_s.getsockname(), message+str(index)))
        c_s.sendall((message+str(index)).encode('utf8')
)

for s in client_sockets:
    data = s.recv(1024)
    print("%s received %s"% (s.getsockname(), data.decode('utf8')))
    if data != "":
        print('closeingsocket', s.getsockname())
        time.sleep(1)
        s.close()