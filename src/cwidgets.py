from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CPushButton(QPushButton):
    def __init__(self, parent=None, *args, **kwargs):
        super(QPushButton, self).__init__(parent, *args, **kwargs)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        shadow = QGraphicsDropShadowEffect()
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setBlurRadius(10)
        self.setGraphicsEffect(shadow)
