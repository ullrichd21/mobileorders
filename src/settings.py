from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cwidgets import CFilePicker

import config


class Settings(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.setWindowTitle("Settings")
        self.setStyleSheet("*{font-size:12px}")
        self.setFixedSize(350, 200)

        vbox = QVBoxLayout()
        row = QHBoxLayout()
        row.addWidget(QLabel("Excel Output Location:"))
        self.file_picker = CFilePicker(default=config.values["output_directory"])

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Default File Name:"))
        self.file_name_input = QLineEdit(config.values["output_file_name"])
        row2.addWidget(self.file_name_input)

        row.addWidget(self.file_picker)
        vbox.addLayout(row)
        vbox.addLayout(row2)
        vbox.addStretch()
        self.setLayout(vbox)

    def closeEvent(self, event):
        config.update_config(
            {"output_directory": self.file_picker.get_file_path(), "output_file_name": self.file_name_input.text()})

        # reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #
        # if reply == QMessageBox.Yes:
        #     event.accept()
        #     print('Window closed')
        # else:
        #     event.ignore()
