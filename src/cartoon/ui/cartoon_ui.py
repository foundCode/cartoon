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
        CartoonWindow.resize(943, 571)
        self.centralwidget = QtWidgets.QWidget(CartoonWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 251, 541))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_edit_search.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.push_button_search = QtWidgets.QPushButton(self.layoutWidget)
        self.push_button_search.setObjectName("push_button_search")
        self.horizontalLayout.addWidget(self.push_button_search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.list_view_cartoon = QtWidgets.QListView(self.layoutWidget)
        self.list_view_cartoon.setObjectName("list_view_cartoon")
        self.verticalLayout.addWidget(self.list_view_cartoon)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(280, 10, 261, 541))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_cartoon_image = QtWidgets.QLabel(self.layoutWidget1)
        self.label_cartoon_image.setMinimumSize(QtCore.QSize(0, 300))
        self.label_cartoon_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cartoon_image.setObjectName("label_cartoon_image")
        self.verticalLayout_2.addWidget(self.label_cartoon_image)
        self.label_cartoon_title = QtWidgets.QLabel(self.layoutWidget1)
        self.label_cartoon_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cartoon_title.setObjectName("label_cartoon_title")
        self.verticalLayout_2.addWidget(self.label_cartoon_title)
        self.list_view_chapter_title = QtWidgets.QListView(self.layoutWidget1)
        self.list_view_chapter_title.setObjectName("list_view_chapter_title")
        self.verticalLayout_2.addWidget(self.list_view_chapter_title)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(560, 10, 371, 541))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scroll_area_show_fragment = QtWidgets.QScrollArea(self.layoutWidget2)
        self.scroll_area_show_fragment.setWidgetResizable(True)
        self.scroll_area_show_fragment.setObjectName("scroll_area_show_fragment")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setObjectName("scroll_area_widget_contents")
        self.label_fragment_image = QtWidgets.QLabel(self.scroll_area_widget_contents)
        self.label_fragment_image.setGeometry(QtCore.QRect(0, 0, 367, 500))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_fragment_image.sizePolicy().hasHeightForWidth())
        self.label_fragment_image.setSizePolicy(sizePolicy)
        self.label_fragment_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fragment_image.setObjectName("label_fragment_image")
        self.scroll_area_show_fragment.setWidget(self.scroll_area_widget_contents)
        self.verticalLayout_3.addWidget(self.scroll_area_show_fragment)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.push_button_previous_fragment = QtWidgets.QPushButton(self.layoutWidget2)
        self.push_button_previous_fragment.setObjectName("push_button_previous_fragment")
        self.horizontalLayout_2.addWidget(self.push_button_previous_fragment)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_chapter_title = QtWidgets.QLabel(self.layoutWidget2)
        self.label_chapter_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_chapter_title.setObjectName("label_chapter_title")
        self.horizontalLayout_2.addWidget(self.label_chapter_title)
        self.line_edit_fragment_index = QtWidgets.QLineEdit(self.layoutWidget2)
        self.line_edit_fragment_index.setObjectName("line_edit_fragment_index")
        self.horizontalLayout_2.addWidget(self.line_edit_fragment_index)
        self.label_num_fragment = QtWidgets.QLabel(self.layoutWidget2)
        self.label_num_fragment.setObjectName("label_num_fragment")
        self.horizontalLayout_2.addWidget(self.label_num_fragment)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.push_button_next_fragment = QtWidgets.QPushButton(self.layoutWidget2)
        self.push_button_next_fragment.setObjectName("push_button_next_fragment")
        self.horizontalLayout_2.addWidget(self.push_button_next_fragment)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(260, 10, 20, 541))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(540, 10, 20, 541))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        CartoonWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CartoonWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 943, 23))
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
        self.label_fragment_image.setText(_translate("CartoonWindow", "显示"))
        self.push_button_previous_fragment.setText(_translate("CartoonWindow", "<"))
        self.label_chapter_title.setText(_translate("CartoonWindow", "("))
        self.line_edit_fragment_index.setText(_translate("CartoonWindow", "0"))
        self.label_num_fragment.setText(_translate("CartoonWindow", "/0)"))
        self.push_button_next_fragment.setText(_translate("CartoonWindow", ">"))
