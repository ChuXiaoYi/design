#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午4:10
# @Author  : cxy
# @Site    : 
# @File    : login_process.py
# @Software: PyCharm
#
from menu import Ui_meun  # 导入uitestPyQt5.ui转换为uitestPyQt5.py中的类
from web_spider_process import Webwindow
from PyQt5 import QtWidgets
import sys


class Menuwindow(QtWidgets.QWidget, Ui_meun):
    # 建立的是Main Window项目，故此处导入的是QMainWindow
    # 参考博客中建立的是Widget项目，因此哪里导入的是QWidget
    def __init__(self):
        super(Menuwindow, self).__init__()
        self.setupUi(self)

    # 菜单点击事件——图片采集
    def start_web_spider(self):  # 定义槽函数btn_click(),也可以理解为重载类Ui_MainWindow中的槽函数btn_click()
        window.close()
        web.show()

    def start_ssh_spider(self):
        pass

    def start_monitor_spider(self):
        pass

    def start_search_spider(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Menuwindow()
    web = Webwindow
    window.show()
    sys.exit(app.exec_())
