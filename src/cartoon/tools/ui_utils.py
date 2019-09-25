import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, QStringListModel


def label_set_image(label, image):
    shape = np.shape(image)
    image = QImage(bytes(image), shape[1], shape[0], shape[1] * 3, QImage.Format_RGB888)
    width = label.width()
    height = label.height()
    pix = QPixmap.fromImage(image)
    resize_pix = pix.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    label.setPixmap(resize_pix)


def list_view_set_string_list(list_view, string_list):
    slm = QStringListModel()
    slm.setStringList(string_list)
    list_view.setModel(slm)


class AsynchronousTask(QThread):
    signal = None

    def __init__(self, task, num_return=0, default_value=None):
        super().__init__()
        self.task = task
        self.num_return = num_return
        self.default_value = default_value

        self.kwargs = None

    def __del__(self):
        self.wait()

    def set_kwargs(self, **kwargs):
        self.kwargs = kwargs

    def run(self):
        if self.kwargs is None:
            outputs = self.task()
        else:
            outputs = self.task(**self.kwargs)
        if self.num_return == 0:
            self.signal.emit()
            return
        if outputs is None:
            outputs = self.default_value
        if self.num_return == 1:
            self.signal.emit(outputs)
            return
        self.signal.emit(list(outputs))
