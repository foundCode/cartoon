# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cartoon_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CartoonWindow(object):
    def setupUi(self, CartoonWindow):
        CartoonWindow.setObjectName("CartoonWindow")
        CartoonWindow.resize(867, 586)
        self.centralwidget = QtWidgets.QWidget(CartoonWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line_edit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_search.setGeometry(QtCore.QRect(10, 10, 171, 20))
        self.line_edit_search.setObjectName("line_edit_search")
        self.push_button_search = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_search.setGeometry(QtCore.QRect(190, 10, 75, 23))
        self.push_button_search.setObjectName("push_button_search")
        self.list_view_cartoon = QtWidgets.QListView(self.centralwidget)
        self.list_view_cartoon.setGeometry(QtCore.QRect(10, 40, 256, 511))
        self.list_view_cartoon.setObjectName("list_view_cartoon")
        self.label_cartoon_image = QtWidgets.QLabel(self.centralwidget)
        self.label_cartoon_image.setGeometry(QtCore.QRect(280, 20, 181, 221))
        self.label_cartoon_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cartoon_image.setObjectName("label_cartoon_image")
        self.label_cartoon_title = QtWidgets.QLabel(self.centralwidget)
        self.label_cartoon_title.setGeometry(QtCore.QRect(280, 260, 181, 16))
        self.label_cartoon_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cartoon_title.setObjectName("label_cartoon_title")
        self.list_view_chapter_title = QtWidgets.QListView(self.centralwidget)
        self.list_view_chapter_title.setGeometry(QtCore.QRect(280, 290, 181, 261))
        self.list_view_chapter_title.setObjectName("list_view_chapter_title")
        self.label_chapter_image = QtWidgets.QLabel(self.centralwidget)
        self.label_chapter_image.setGeometry(QtCore.QRect(490, 20, 361, 501))
        self.label_chapter_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_chapter_image.setObjectName("label_chapter_image")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(490, 530, 361, 24))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(500, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_chapter_title = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_chapter_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_chapter_title.setObjectName("label_chapter_title")
        self.horizontalLayout_2.addWidget(self.label_chapter_title)
        self.line_edit_now_chapter_section = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.line_edit_now_chapter_section.setObjectName("line_edit_now_chapter_section")
        self.horizontalLayout_2.addWidget(self.line_edit_now_chapter_section)
        self.label_num_chapter_section = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_num_chapter_section.setObjectName("label_num_chapter_section")
        self.horizontalLayout_2.addWidget(self.label_num_chapter_section)
        spacerItem1 = QtWidgets.QSpacerItem(500, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        CartoonWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CartoonWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 23))
        self.menubar.setObjectName("menubar")
        CartoonWindow.setMenuBar(self.menubar)

        self.retranslateUi(CartoonWindow)
        QtCore.QMetaObject.connectSlotsByName(CartoonWindow)

    def retranslateUi(self, CartoonWindow):
        _translate = QtCore.QCoreApplication.translate
        CartoonWindow.setWindowTitle(_translate("CartoonWindow", "36mh.com"))
        self.push_button_search.setText(_translate("CartoonWindow", "搜索"))
        self.label_cartoon_image.setText(_translate("CartoonWindow", "漫画"))
        self.label_cartoon_title.setText(_translate("CartoonWindow", "漫画名"))
        self.label_chapter_image.setText(_translate("CartoonWindow", "显示"))
        self.label_chapter_title.setText(_translate("CartoonWindow", "("))
        self.line_edit_now_chapter_section.setText(_translate("CartoonWindow", "0"))
        self.label_num_chapter_section.setText(_translate("CartoonWindow", "/0)"))
