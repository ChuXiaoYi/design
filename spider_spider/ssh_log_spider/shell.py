# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys
import shutil
import json
import paramiko


def ssh_scp_put(ip, username, password):
    """
    上传文件
    :param ip:
    :param port:
    :param user:
    :param password:
    :param local_file:
    :param remote_file:
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, username, password)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.put('/Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/ssh_log_spider/shell.py', '/home/spider/shell.py')
    print('上传完成')


def ssh_scp_get(ip, user, password):
    """
    下载文件
    :param ip:
    :param user:
    :param password:
    :return:
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, user, password)
    a = ssh.exec_command('date')
    stdin, stdout, stderr = a
    print(stdout.read())
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    sftp.get('/home/spider/chuxiaoyi/result.json',
             '/Users/chuxiaoyi/python/练习/code/毕设/design/spider_spider/ssh_log_spider/ssh_result/agoda-20180521/' + ip + '.json')
    print("下载完成")


def telent(ip):
    """
    远程连接服务器
    :return:
    """
    Host = ip
    username = 'spider'
    password = 'spider'

    from pexpect import pxssh
    ssh = pxssh.pxssh()
    ssh.login(server=Host, username=username, password=password)
    ssh.sendline('python shell.py agodaHotel')
    ssh.prompt()
    print(ssh.before)


def create_self_file():
    """
    创建自己的目录
    :return:
    """
    dir_list = os.listdir('/home/spider')
    if "chuxiaoyi" in dir_list:
        shutil.rmtree('/home/spider/chuxiaoyi')
    os.mkdir('chuxiaoyi')


def get_log():
    """
    获取日志
    :return:
    """
    p = subprocess.Popen(args='ls /search/spider_log/rotation/', shell=True, stdout=subprocess.PIPE)
    # 当前文件夹获取到的日志文件夹
    log_files = p.stdout.read().decode('utf8').split('\n')
    # 需要查看的日志文件夹
    need_log_files = ['20180521']
    for f in log_files:
        if f in need_log_files:
            os.chdir('/search/spider_log/rotation/' + f)
            for hotel in sys.argv[1:]:
                cmd = u'grep -r "' + hotel + u'" | grep "爬虫反馈 code:" > /home/spider/chuxiaoyi/' + hotel + u'-' + f + u'.txt'
                p = subprocess.Popen(args=cmd.encode('utf8'),
                                     shell=True,
                                     universal_newlines=True)

                p.wait()


def process_log():
    """
    解析日志信息
    :return:
    """
    dir_list = os.listdir('/home/spider/chuxiaoyi')
    # 当前服务器的所有符合条件的日志
    all_log_list = list()
    # 当前服务器的所有符合条件的爬虫code字典合
    all_code_dict = dict()
    for d in dir_list:
        with open('/home/spider/chuxiaoyi/' + d, 'r') as f:
            # 当前日期的日志
            log_list = list()
            # 保存code
            code_dict = dict()
            for info in f.readlines():
                try:
                    code = re.search(r'code: (\d+)', info).group(1)
                except Exception as e:
                    code = ''
                try:
                    source = re.search(r'source: (.*)] ', info).group(1)
                except Exception:
                    source = ''
                try:
                    content = re.search(r'"content": "(.*)", "task_type"', info).group(1)
                except Exception as e:
                    content = ""
                code_dict[code] = code_dict.get(code, 0) + 1
                all_code_dict[code] = all_code_dict.get(code, 0) + 1
                spider_info = dict(
                    code=code,
                    source=source,
                    content=content
                )
                log_list.append(spider_info)
        all_log_list.append(
            dict(
                data=d.split('.')[0],
                count=code_dict,
                log_list=log_list
            )
        )
    with open('/home/spider/chuxiaoyi/result.json', 'w') as result:
        result.write(
            json.dumps(all_log_list, ensure_ascii=False)
        )
    print(all_code_dict)


def main():
    if len(sys.argv) == 1:
        ips = ['10.10.155.184', '10.10.218.206', '10.10.215.193', '10.10.231.156', '10.10.234.200']
        for i in range(len(ips)):
            ssh_scp_put(ips[i], username='spider', password='spider')
            telent(ips[i])
            ssh_scp_get(ips[i], 'spider', 'spider')
    if len(sys.argv) > 1:
        create_self_file()
        get_log()
        process_log()


if __name__ == '__main__':
    main()
