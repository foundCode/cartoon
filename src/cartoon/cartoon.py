# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from cartoon_ui import Ui_CartoonWindow
from cartoon_36mh import Cartoon36mh
from utils import get_image_by_url
from ui_utils import label_set_image


class LoadCartoon:
    def __init__(self):
        self.cartoon_36mh = Cartoon36mh()
        self.cartoon_title_url = []
        self.cartoon_index = -1

        self.cartoon_image_url = None

        self.chapter_title_url = []
        self.chapter_index = -1

        self.chapter_image_urls = []
        self.now_chapter_section = -1
        self.num_chapter_section = -1

    def search(self, search_text):
        if len(search_text) == 0:
            return []
        cartoon_urls, cartoon_titles = self.cartoon_36mh.search(search_text)
        self.cartoon_title_url.clear()
        num_cartoon = len(cartoon_urls)
        for i in range(num_cartoon):
            self.cartoon_title_url.append({'title': cartoon_titles[i], 'url': cartoon_urls[i]})
        return cartoon_titles

    def update_cartoon(self, cartoon_index):
        assert 0 <= cartoon_index < len(self.cartoon_title_url)
        self.cartoon_index = cartoon_index
        title_url = self.cartoon_title_url[self.cartoon_index]
        print(title_url)
        cartoon_title, cartoon_url = title_url['title'], title_url['url']
        self.cartoon_image_url, _ = self.cartoon_36mh.get_cartoon_data(cartoon_url)

        chapter_titles, chapter_urls = self.cartoon_36mh.get_chapters(cartoon_url)

        self.chapter_title_url.clear()
        num_chapter = len(chapter_urls)
        for i in range(num_chapter):
            self.chapter_title_url.append({'title': chapter_titles[i], 'url': chapter_urls[i]})

    def update_chapter(self, chapter_index):
        assert 0 <= chapter_index < len(self.chapter_title_url)
        self.chapter_index = chapter_index
        title_url = self.chapter_title_url[self.chapter_index]
        print(title_url)
        chapter_title, chapter_url = title_url['title'], title_url['url']
        self.chapter_image_urls = self.cartoon_36mh.get_chapter_image_urls(chapter_url)

        self.now_chapter_section = 1
        self.num_chapter_section = len(self.chapter_image_urls)

    def get_cartoon_title_url(self):
        title_url = self.cartoon_title_url[self.cartoon_index]
        return title_url['title'], title_url['url']

    def get_chapter_title_url(self):
        title_url = self.chapter_title_url[self.cartoon_index]
        return title_url['title'], title_url['url']

    def get_cartoon_image(self):
        return get_image_by_url(self.cartoon_image_url)

    def get_chapter_image(self, chapter_section=-1):
        if chapter_section != -1:
            self.now_chapter_section = chapter_section
        return get_image_by_url(self.chapter_image_urls[self.now_chapter_section])


class CartoonUI(QtWidgets.QMainWindow, Ui_CartoonWindow):
    def __init__(self):
        super(CartoonUI, self).__init__()
        self.setupUi(self)

        self.cartoon_36mh = Cartoon36mh()
        self.cartoon_title_url = []
        self.cartoon_index = -1

        self.chapter_title_url = []
        self.chapter_index = -1

        self.chapter_image_urls = []
        self.now_chapter_section = -1
        self.num_chapter_section = -1

        self.init_ui()

    def init_ui(self):
        self.line_edit_search.setText('愉快的失忆')
        self.line_edit_search.returnPressed.connect(self.push_button_search_clicked)
        self.push_button_search.clicked.connect(self.push_button_search_clicked)
        self.list_view_cartoon.doubleClicked.connect(self.list_view_cartoon_double_clicked)
        self.list_view_chapter_title.doubleClicked.connect(self.list_view_chapter_title_double_clicked)
        self.line_edit_now_chapter_section.returnPressed.connect(self.line_edit_now_chapter_section_return_pressed)

        self.list_view_cartoon.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_view_chapter_title.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.line_edit_now_chapter_section.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[0-9]*[1-9][0-9]*$')))

    @QtCore.pyqtSlot(name='push_button_search_clicked')
    def push_button_search_clicked(self):
        search_text = self.line_edit_search.text()
        if len(search_text) == 0:
            return

        cartoon_urls, cartoon_titles = self.cartoon_36mh.search(search_text)
        slm = QtCore.QStringListModel()
        slm.setStringList(cartoon_titles)
        self.list_view_cartoon.setModel(slm)

        self.cartoon_title_url.clear()
        num_cartoon = len(cartoon_urls)
        for i in range(num_cartoon):
            self.cartoon_title_url.append({'title': cartoon_titles[i], 'url': cartoon_urls[i]})

    def list_view_cartoon_double_clicked(self, mode_index):
        self.chapter_title_url = []
        self.cartoon_index = mode_index.row()
        self.chapter_image_urls = []
        self.now_chapter_section = -1
        self.num_chapter_section = -1
        self.update_cartoon()

    def update_cartoon(self):
        title_url = self.cartoon_title_url[self.cartoon_index]
        print(title_url)
        cartoon_title, cartoon_url = title_url['title'], title_url['url']
        cartoon_image_url, _ = self.cartoon_36mh.get_cartoon_data(cartoon_url)
        cartoon_image = get_image_by_url(cartoon_image_url)[:, :, ::-1]

        label_set_image(self.label_cartoon_image, cartoon_image)
        self.label_cartoon_title.setText(cartoon_title)

        chapter_titles, chapter_urls = self.cartoon_36mh.get_chapters(cartoon_url)
        slm = QtCore.QStringListModel()
        slm.setStringList(chapter_titles)
        self.list_view_chapter_title.setModel(slm)

        self.chapter_title_url.clear()
        num_chapter = len(chapter_urls)
        for i in range(num_chapter):
            self.chapter_title_url.append({'title': chapter_titles[i], 'url': chapter_urls[i]})

    def list_view_chapter_title_double_clicked(self, model_index):
        self.now_chapter_section = -1
        self.num_chapter_section = -1
        self.chapter_index = model_index.row()
        self.update_chapter()

    def update_chapter(self):
        title_url = self.chapter_title_url[self.chapter_index]
        print(title_url)
        chapter_title, chapter_url = title_url['title'], title_url['url']
        self.chapter_image_urls = self.cartoon_36mh.get_chapter_image_urls(chapter_url)

        self.now_chapter_section = 1
        self.num_chapter_section = len(self.chapter_image_urls)
        self.show_chapter_image()

    def show_chapter_image(self):
        if self.now_chapter_section > self.num_chapter_section:
            return
        print(self.now_chapter_section, self.chapter_image_urls[self.now_chapter_section - 1])
        label_set_image(self.label_chapter_image,
                        get_image_by_url(self.chapter_image_urls[self.now_chapter_section - 1])[:, :, ::-1])
        self.label_chapter_title.setText('{}  ('.format(self.chapter_title_url[self.chapter_index]['title']))
        self.line_edit_now_chapter_section.setText(str(self.now_chapter_section))
        self.label_num_chapter_section.setText('/{})'.format(self.num_chapter_section))

    @QtCore.pyqtSlot(name='line_edit_now_chapter_section_return_pressed')
    def line_edit_now_chapter_section_return_pressed(self):
        now_chapter_section = int(self.line_edit_now_chapter_section.text())
        if 1 <= now_chapter_section <= self.num_chapter_section and now_chapter_section != self.now_chapter_section:
            self.now_chapter_section = now_chapter_section
            self.show_chapter_image()

    def keyPressEvent(self, event):
        if self.num_chapter_section == -1:
            return
        if event.key() == QtCore.Qt.Key_Right:
            if self.now_chapter_section < self.num_chapter_section:
                self.now_chapter_section += 1
                self.show_chapter_image()
            elif self.chapter_index + 1 < len(self.chapter_title_url):
                self.chapter_index += 1
                self.update_chapter()
        elif event.key() == QtCore.Qt.Key_Left:
            if self.now_chapter_section > 1:
                self.now_chapter_section -= 1
                self.show_chapter_image()
            elif self.chapter_index - 1 >= 0:
                self.chapter_index -= 1
                self.update_chapter()

    def close(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    cartoon_ui = CartoonUI()
    cartoon_ui.show()

    sys.exit(app.exec_())
