from watchdog.observers import Observer
from watchdog.events import *
import time
import smtplib
from email.header import Header
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"      # SMTP服务器

sender = '895706056@qq.com'    # 发件人邮箱(最好写全, 不然会失败)
receivers = ['a895706056@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


title = '文件监控结果'  # 邮件主题

def sendEmail(content):

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login('895706056@qq.com', 'mqscgaxzmrkqbfga')  # 登录验证， 密码要每天更新
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

def get_file_size(file_name):
    """
    获取文件大小
    :param file_name:
    :return:
    """
    if os.path.exists(file_name):
        bytes_size = float(os.path.getsize(file_name))
        kb = bytes_size/1024
        mb = kb/1024
        return mb
    return 0

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            content = "文件夹从{0}移动到{1}".format(event.src_path, event.dest_path)
            print(content)
            sendEmail(content)
        else:
            content = "文件从{0}移到{1}".format(event.src_path, event.dest_path)
            print(content)
            sendEmail(content)

    def on_created(self, event):
        if event.is_directory:
            content = ("文件夹创建路径：{0}".format(event.src_path))
            print(content)
            sendEmail(content)
        else:
            content = ("文件创建路径：{0}".format(event.src_path))
            print(content)
            sendEmail(content)

    def on_deleted(self, event):
        if event.is_directory:
            content = ("文件夹已删除：{0}".format(event.src_path))
            print(content)
            sendEmail(content)
        else:
            content = ("文件已删除：{0}".format(event.src_path))
            print(content)
            sendEmail(content)

    def on_modified(self, event):
        if event.is_directory:
            content = ("文件夹已修改：{0}".format(event.src_path))
            print(content)
            sendEmail(content)
        else:
            content = ("文件已修改：{0}".format(event.src_path))
            size = get_file_size(event.src_path)
            print(content,'文件大小：{size}'.format(size=size))
            sendEmail(content+'文件大小：{size}'.format(size=size))

if __name__ == '__main__':
    observer = Observer()
    event_handler = FileEventHandler()
    print("开始监听")
    observer.schedule(event_handler,
                      "/Users/chuxiaoyi/python/练习/code/毕设/design/image",
                      True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    # sendEmail('text')