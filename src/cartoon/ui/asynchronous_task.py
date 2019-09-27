import numpy as np
from PyQt5.QtCore import pyqtSignal

from tools.ui_utils import AsynchronousTask


class TaskSearch(AsynchronousTask):
    signal = pyqtSignal()

    def __init__(self, task):
        super().__init__(task)


class TaskSelectCartoon(AsynchronousTask):
    signal = pyqtSignal()

    def __init__(self, task):
        super().__init__(task)


class TaskSelectChapter(AsynchronousTask):
    signal = pyqtSignal()

    def __init__(self, task):
        super().__init__(task)


class TaskLoadFragment(AsynchronousTask):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, task):
        super().__init__(task, 1, np.zeros([1], dtype=np.uint8))
