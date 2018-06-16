# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_meun(object):
    def setupUi(self, meun):
        meun.setObjectName("meun")
        meun.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(meun)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ssh_spider = QtWidgets.QPushButton(meun)
        self.ssh_spider.setObjectName("ssh_spider")
        self.verticalLayout.addWidget(self.ssh_spider)
        self.web_spider = QtWidgets.QPushButton(meun)
        self.web_spider.setObjectName("web_spider")
        self.verticalLayout.addWidget(self.web_spider)
        self.monitor_spider = QtWidgets.QPushButton(meun)
        self.monitor_spider.setObjectName("monitor_spider")
        self.verticalLayout.addWidget(self.monitor_spider)
        self.search_spider = QtWidgets.QPushButton(meun)
        self.search_spider.setObjectName("search_spider")
        self.verticalLayout.addWidget(self.search_spider)

        self.retranslateUi(meun)
        self.ssh_spider.clicked.connect(meun.start_ssh_spider)
        self.web_spider.clicked.connect(meun.start_web_spider)
        self.monitor_spider.clicked.connect(meun.start_monitor_spider)
        self.search_spider.clicked.connect(meun.start_search_spider)
        QtCore.QMetaObject.connectSlotsByName(meun)

    def retranslateUi(self, meun):
        _translate = QtCore.QCoreApplication.translate
        meun.setWindowTitle(_translate("meun", "菜单栏"))
        self.ssh_spider.setText(_translate("meun", "远程日志采集"))
        self.web_spider.setText(_translate("meun", "图片采集"))
        self.monitor_spider.setText(_translate("meun", "文件监控"))
        self.search_spider.setText(_translate("meun", "全文检索"))

