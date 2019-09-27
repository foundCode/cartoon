import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from core.cartoon import get_init_image, LoadCartoon
from ui.cartoon_ui import Ui_CartoonWindow
from ui.asynchronous_task import *
from tools.ui_utils import label_set_image, list_view_set_string_list

CURRENT_FRAGMENT = -1
PREVIOUS_FRAGMENT = -2
NEXT_FRAGMENT = -3


class CartoonUI(QtWidgets.QMainWindow, Ui_CartoonWindow):
    def __init__(self):
        super(CartoonUI, self).__init__()
        self.setupUi(self)

        self.init_image = get_init_image()
        self.load_cartoon = LoadCartoon()

        self.init_ui()

        self.mini_fragment_height = 0
        self.task_search = TaskSearch(self.load_cartoon.search)
        self.task_search.signal.connect(self.update_list_view_cartoon)
        self.task_select_cartoon = TaskSelectCartoon(self.load_cartoon.select_cartoon)
        self.task_select_cartoon.signal.connect(self.show_cartoon)
        self.task_select_chapter = TaskSelectChapter(self.load_cartoon.select_chapter)
        self.task_select_chapter.signal.connect(self.update_fragment_image)
        self.task_load_fragment = TaskLoadFragment(self.load_cartoon.get_fragment_image)
        self.task_load_fragment.signal.connect(self.show_fragment_image)

    def init_ui(self):
        self.line_edit_search.setText('愉快的失忆')
        self.line_edit_search.returnPressed.connect(self.push_button_search_clicked)
        self.push_button_search.clicked.connect(self.push_button_search_clicked)
        self.list_view_cartoon.doubleClicked.connect(self.list_view_cartoon_double_clicked)
        self.list_view_chapter_title.doubleClicked.connect(self.list_view_chapter_title_double_clicked)
        self.line_edit_fragment_index.returnPressed.connect(self.line_edit_fragment_index_return_pressed)
        self.push_button_previous_fragment.clicked.connect(self.push_button_previous_fragment_clicked)
        self.push_button_next_fragment.clicked.connect(self.push_button_next_fragment_clicked)

        self.list_view_cartoon.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_view_chapter_title.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.line_edit_fragment_index.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[0-9]*[1-9][0-9]*$')))

    def init_cartoon(self):
        label_set_image(self.label_cartoon_image, self.init_image)
        self.label_cartoon_title.setText('漫画名')
        self.list_view_chapter_title.setModel(QtCore.QStringListModel())
        self.init_fragment()

    def init_fragment(self):
        label_set_image(self.label_fragment_image, self.init_image)
        self.label_chapter_title.setText('{}  ('.format('0 话'))
        self.line_edit_fragment_index.setText(str(0))
        self.label_num_fragment.setText('/{})'.format(0))

        self.push_button_previous_fragment.setEnabled(False)
        self.push_button_next_fragment.setEnabled(False)
        self.line_edit_fragment_index.setFocusPolicy(QtCore.Qt.NoFocus)

    @QtCore.pyqtSlot(name='push_button_search_clicked')
    def push_button_search_clicked(self):
        self.push_button_search.setEnabled(False)
        search_text = self.line_edit_search.text()
        if len(search_text) == 0:
            self.push_button_search.setEnabled(True)
            return
        self.task_search.set_kwargs(search_text=search_text)
        self.task_search.start()

    def list_view_cartoon_double_clicked(self, model_index):
        self.init_cartoon()
        self.task_select_cartoon.set_kwargs(cartoon_index=model_index.row())
        self.task_select_cartoon.start()

    def list_view_chapter_title_double_clicked(self, model_index):
        self.init_fragment()
        self.task_select_chapter.set_kwargs(chapter_index=model_index.row())
        self.task_select_chapter.start()

    @QtCore.pyqtSlot(name='push_button_previous_fragment_clicked')
    def push_button_previous_fragment_clicked(self):
        self.update_fragment_image(PREVIOUS_FRAGMENT)

    @QtCore.pyqtSlot(name='line_edit_fragment_index_return_pressed')
    def line_edit_fragment_index_return_pressed(self):
        fragment_index = int(self.line_edit_fragment_index.text())
        self.update_fragment_image(fragment_index - 1)

    @QtCore.pyqtSlot(name='push_button_next_fragment_clicked')
    def push_button_next_fragment_clicked(self):
        self.update_fragment_image(NEXT_FRAGMENT)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.update_fragment_image(NEXT_FRAGMENT)
        elif event.key() == QtCore.Qt.Key_Left:
            self.update_fragment_image(PREVIOUS_FRAGMENT)

    def update_list_view_cartoon(self):
        self.push_button_search.setEnabled(True)
        list_view_set_string_list(self.list_view_cartoon, self.load_cartoon.cartoon_titles)

    def show_cartoon(self):
        label_set_image(self.label_cartoon_image, self.load_cartoon.get_cartoon_image())
        cartoon_title = self.load_cartoon.get_cartoon_title_url()['title']
        self.label_cartoon_title.setText(cartoon_title)

        list_view_set_string_list(self.list_view_chapter_title, self.load_cartoon.chapter_titles)

    def update_fragment_image(self, fragment_index=LoadCartoon.CURRENT_FRAGMENT):
        self.push_button_previous_fragment.setEnabled(False)
        self.push_button_next_fragment.setEnabled(False)
        self.line_edit_fragment_index.setFocusPolicy(QtCore.Qt.NoFocus)
        self.task_load_fragment.set_kwargs(fragment_index=fragment_index)
        self.task_load_fragment.start()

    def show_fragment_image(self, fragment_image=None):
        self.push_button_previous_fragment.setEnabled(True)
        self.push_button_next_fragment.setEnabled(True)
        self.line_edit_fragment_index.setFocusPolicy(QtCore.Qt.ClickFocus)
        if np.ndim(fragment_image) < 2:
            return

        label_width = self.label_fragment_image.width()
        image_height, image_width = np.shape(fragment_image)[:2]
        label_height = min(self.mini_fragment_height, round(label_width * (image_height / image_width)))
        self.label_fragment_image.setFixedHeight(label_height)
        self.scroll_area_widget_contents.setFixedHeight(label_height)
        self.scroll_area_show_fragment.verticalScrollBar().setValue(0)

        label_set_image(self.label_fragment_image, fragment_image)
        self.label_chapter_title.setText('{}  ('.format(self.load_cartoon.get_chapter_title_url()['title']))
        self.line_edit_fragment_index.setText(str(self.load_cartoon.fragment_index + 1))
        self.label_num_fragment.setText('/{})'.format(self.load_cartoon.num_fragment))

    def show(self):
        super().show()
        # 在 show 前进行初始化时，使用 label 显示的图像不会随 label 的大小进行缩放
        # label 的 width 和 height 在 show 前没有更新
        self.init_cartoon()
        self.mini_fragment_height = self.label_fragment_image.height()

    def closeEvent(self, *args, **kwargs):
        self.load_cartoon.close()
        print('close')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    cartoon_ui = CartoonUI()
    cartoon_ui.show()

    sys.exit(app.exec_())
