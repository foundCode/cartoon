import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from core.cartoon import get_init_image, LoadCartoon
from ui.cartoon_ui import Ui_CartoonWindow
from tools.ui_utils import label_set_image

CURRENT_FRAGMENT = -1
PREVIOUS_FRAGMENT = -2
NEXT_FRAGMENT = -3


class CartoonUI(QtWidgets.QMainWindow, Ui_CartoonWindow):
    def __init__(self):
        super(CartoonUI, self).__init__()
        self.setupUi(self)

        self.init_image = get_init_image()

        self.load_cartoon = LoadCartoon()
        self.cartoon_titles = []
        self.chapter_titles = []

        self.init_ui()

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

        self.init_cartoon()

    def init_cartoon(self):
        label_set_image(self.label_cartoon_image, self.init_image)
        self.label_cartoon_title.setText('漫画名称')
        self.list_view_chapter_title.setModel(QtCore.QStringListModel())
        self.init_fragment()

    def init_fragment(self):
        label_set_image(self.label_fragment_image, self.init_image)
        self.label_chapter_title.setText('{}  ('.format('0 话'))
        self.line_edit_fragment_index.setText(str(0))
        self.label_num_fragment.setText('/{})'.format(0))

    @QtCore.pyqtSlot(name='push_button_search_clicked')
    def push_button_search_clicked(self):
        search_text = self.line_edit_search.text()
        if len(search_text) == 0:
            return

        self.cartoon_titles = self.load_cartoon.search(search_text)
        slm = QtCore.QStringListModel()
        slm.setStringList(self.cartoon_titles)
        self.list_view_cartoon.setModel(slm)

    def list_view_cartoon_double_clicked(self, model_index):
        self.init_cartoon()
        self.chapter_titles = self.load_cartoon.select_cartoon(model_index.row())
        self.show_cartoon()

    def list_view_chapter_title_double_clicked(self, model_index):
        self.init_fragment()
        self.load_cartoon.select_chapter(model_index.row())
        self.show_fragment_image()

    @QtCore.pyqtSlot(name='push_button_previous_fragment_clicked')
    def push_button_previous_fragment_clicked(self):
        self.show_fragment_image(PREVIOUS_FRAGMENT)

    @QtCore.pyqtSlot(name='line_edit_fragment_index_return_pressed')
    def line_edit_fragment_index_return_pressed(self):
        fragment_index = int(self.line_edit_fragment_index.text())
        self.show_fragment_image(fragment_index - 1)

    @QtCore.pyqtSlot(name='push_button_next_fragment_clicked')
    def push_button_next_fragment_clicked(self):
        self.show_fragment_image(NEXT_FRAGMENT)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.show_fragment_image(NEXT_FRAGMENT)
        elif event.key() == QtCore.Qt.Key_Left:
            self.show_fragment_image(PREVIOUS_FRAGMENT)

    def show_cartoon(self):
        label_set_image(self.label_cartoon_image, self.load_cartoon.get_cartoon_image())
        cartoon_title = self.load_cartoon.get_cartoon_title_url()['title']
        self.label_cartoon_title.setText(cartoon_title)

        slm = QtCore.QStringListModel()
        slm.setStringList(self.chapter_titles)
        self.list_view_chapter_title.setModel(slm)

    def show_fragment_image(self, fragment=CURRENT_FRAGMENT):
        fragment_image = None
        if fragment == CURRENT_FRAGMENT:
            fragment_image = self.load_cartoon.get_current_fragment_image()
        elif fragment == PREVIOUS_FRAGMENT:
            fragment_image = self.load_cartoon.get_previous_fragment_image()
        elif fragment == NEXT_FRAGMENT:
            fragment_image = self.load_cartoon.get_next_fragment_image()
        elif fragment >= 0:
            fragment_image = self.load_cartoon.get_current_fragment_image(fragment)
        if fragment_image is None:
            return
        label_set_image(self.label_fragment_image, fragment_image)
        self.label_chapter_title.setText('{}  ('.format(self.load_cartoon.get_chapter_title_url()['title']))
        self.line_edit_fragment_index.setText(str(self.load_cartoon.fragment_index + 1))
        self.label_num_fragment.setText('/{})'.format(self.load_cartoon.num_fragment))

    def close(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    cartoon_ui = CartoonUI()
    cartoon_ui.show()

    sys.exit(app.exec_())
