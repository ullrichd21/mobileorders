from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class CPushButton(QPushButton):
    def __init__(self, parent=None, *args, **kwargs):
        super(QPushButton, self).__init__(parent, *args, **kwargs)

        self.setStyleSheet("padding: 5px")

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        shadow = QGraphicsDropShadowEffect()
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setBlurRadius(10)
        self.setGraphicsEffect(shadow)


class CFilePicker(QWidget):
    def __init__(self, parent=None, default=None, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)

        self.line = QLineEdit()
        if default is not None:
            self.line.setText(default)
        self.button = CPushButton("Open", clicked=lambda: self.line.setText(QFileDialog().getExistingDirectory()))
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox = QHBoxLayout()
        hbox.addWidget(self.line)
        hbox.addWidget(self.button)
        self.setLayout(hbox)

    def get_file_path(self):
        return self.line.text()


class CAddItemWidget(QWidget):
    def __init__(self, parent=None, add_clicked=None, remove_clicked=None, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)

        hbox = QHBoxLayout()
        hbox.addStretch()

        if remove_clicked is not None:
            self.remove_button = CPushButton("-", clicked=remove_clicked)
            hbox.addWidget(self.remove_button)

        if add_clicked is not None:
            self.add_button = CPushButton("+", clicked=add_clicked)
            hbox.addWidget(self.add_button)

        self.setLayout(hbox)
