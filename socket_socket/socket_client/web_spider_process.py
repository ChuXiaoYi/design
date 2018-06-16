#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午4:10
# @Author  : cxy
# @Site    :
# @File    : login_process.py
# @Software: PyCharm
#
from web_spider import Ui_web_spider  # 导入uitestPyQt5.ui转换为uitestPyQt5.py中的类

from PyQt5.QtWidgets import QDialog, QApplication
import sys


class Webwindow(QDialog, Ui_web_spider):
    # 建立的是Main Window项目，故此处导入的是QMainWindow
    # 参考博客中建立的是Widget项目，因此哪里导入的是QWidget
    def __init__(self):
        super(Webwindow, self).__init__()
        self.setupUi(self)

    def start_spider(self):  # 定义槽函数btn_click(),也可以理解为重载类Ui_MainWindow中的槽函数btn_click()
        web_url = self.web_url.text()
        deep = self.deep.text()
        image_path = self.image_path.text()
        is_download = self.is_download.text()
        info = dict(
            web_url=web_url,
            deep=deep,
            image_path=image_path,
            is_download=is_download
        )
        import socket_client
        result = socket_client.main(2, info)
        print(result)
        self.textEdit.setText("数据采集已完成")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Webwindow()
    print(type(window))
    window.exec()
    sys.exit(app.exec_())
