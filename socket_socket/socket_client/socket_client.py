# -*- coding: utf-8 -*-
import socket
import time
import json


def choose_spider(num, kwargs):
    """
    判断要执行哪个爬虫
    :return:
    """
    global data_dict
    if num == 0:
        # ssh_log_spider
        data_dict = dict(
            num=num
        )
    elif num == 1:
        # monitor_spider
        watch_file = input("请输入要监控的文件路径：")
        data_dict = dict(
            num=num,
            watch_file=watch_file
        )
    elif num == 2:
        # web_spider
        web_url = kwargs['web_url']
        deep = kwargs['deep']
        is_download = kwargs['is_download']
        if is_download == 'yes':
            image_path = kwargs['image_path']
            data_dict = dict(
                num=num,
                web_url=web_url,
                deep=deep,
                image_path=image_path
            )
        else:
            data_dict = dict(
                num=num,
                web_url=web_url,
                deep=deep
            )
    elif num == 3:
        # search_spider
        file = input('请输入检索文件夹路径：')
        key_word = input('请输入关键词：')
        data_dict = dict(
            num=num,
            file=file,
            key_word=key_word
        )
    else:
        pass
    data = json.dumps(data_dict, ensure_ascii=False)
    return data


def main(num, info):
    """
    主程序
    :param num:
    :return:
    """
    server_address = ('127.0.0.1', 8888)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("正在连接%s，端口号为%s" % server_address)
    client_socket.connect(server_address)
    data = choose_spider(int(num), info)
    print(data)
    client_socket.sendall(data.encode('utf8'))
    result = client_socket.recv(65535)
    print("%s received %s" % (client_socket.getsockname(), result.decode('utf8')))
    if data != "":
        print('closeingsocket', client_socket.getsockname())
        time.sleep(1)
        client_socket.close()
    return result


def login():
    """
    用户登陆
    :return:
    """
    while True:
        username = input('请输入用户名：')
        password = int(input('请输入密码：'))
        if username != 'cxy' or password != 123:
            print('用户名或密码错误，请重新输入。。')
        else:
            print('登陆成功。。。')
            break


if __name__ == '__main__':
    login()
    while True:
        num = input("输入你想请求的spider：\n"
                    "\t0: ssh_log_spider\n"
                    "\t1: monitor_spider\n"
                    "\t2: web_spider\n"
                    "\t3: search_spider\n")
        main(num)

