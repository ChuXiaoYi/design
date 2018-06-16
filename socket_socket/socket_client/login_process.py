#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午4:10
# @Author  : cxy
# @Site    : 
# @File    : login_process.py
# @Software: PyCharm
#
from login import Ui_MainWindow  # 导入uitestPyQt5.ui转换为uitestPyQt5.py中的类
from menu_process import Menuwindow
from PyQt5 import QtWidgets
import sys


class Mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # 建立的是Main Window项目，故此处导入的是QMainWindow
    # 参考博客中建立的是Widget项目，因此哪里导入的是QWidget
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)

    def btn_click(self):  # 定义槽函数btn_click(),也可以理解为重载类Ui_MainWindow中的槽函数btn_click()
        # pass
        name = self.username.text()
        password = self.password.text()
        if name == 'cxy' and password == '123':
            self.close()
            menu.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Mywindow()
    menu = Menuwindow()
    window.show()
    sys.exit(app.exec_())
