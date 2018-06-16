# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'web_spider.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_web_spider(object):
    def setupUi(self, web_spider):
        web_spider.setObjectName("web_spider")
        web_spider.resize(400, 300)
        self.formLayout_2 = QtWidgets.QFormLayout(web_spider)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(web_spider)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.web_url = QtWidgets.QLineEdit(web_spider)
        self.web_url.setObjectName("web_url")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.web_url)
        self.label_2 = QtWidgets.QLabel(web_spider)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.deep = QtWidgets.QLineEdit(web_spider)
        self.deep.setObjectName("deep")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.deep)
        self.label_3 = QtWidgets.QLabel(web_spider)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.is_download = QtWidgets.QLineEdit(web_spider)
        self.is_download.setObjectName("is_download")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.is_download)
        self.label_4 = QtWidgets.QLabel(web_spider)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.image_path = QtWidgets.QLineEdit(web_spider)
        self.image_path.setObjectName("image_path")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.image_path)
        self.pushButton = QtWidgets.QPushButton(web_spider)
        self.pushButton.setObjectName("pushButton")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.pushButton)
        self.label_5 = QtWidgets.QLabel(web_spider)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.textEdit = QtWidgets.QTextEdit(web_spider)
        self.textEdit.setObjectName("textEdit")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.textEdit)

        self.retranslateUi(web_spider)
        self.pushButton.clicked.connect(web_spider.start_spider)
        QtCore.QMetaObject.connectSlotsByName(web_spider)

    def retranslateUi(self, web_spider):
        _translate = QtCore.QCoreApplication.translate
        web_spider.setWindowTitle(_translate("web_spider", "图片采集"))
        self.label.setText(_translate("web_spider", "请输入要爬取的网站："))
        self.label_2.setText(_translate("web_spider", "请输入爬取深度："))
        self.label_3.setText(_translate("web_spider", "是否下载图片："))
        self.label_4.setText(_translate("web_spider", "保存路径："))
        self.pushButton.setText(_translate("web_spider", "开始爬取"))
        self.label_5.setText(_translate("web_spider", "结果："))

