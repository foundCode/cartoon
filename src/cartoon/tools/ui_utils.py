import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


def label_set_image(label, image):
    shape = np.shape(image)
    image = QImage(bytes(image), shape[1], shape[0], shape[1] * 3, QImage.Format_RGB888)
    width = label.width()
    height = label.height()
    pix = QPixmap.fromImage(image)
    resize_pix = pix.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    label.setPixmap(resize_pix)
