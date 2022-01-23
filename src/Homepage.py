from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cwidgets import CPushButton
from Form import *
from settings import Settings

class Homepage(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("Mobile Order")

        self.stack = QStackedWidget()
        self.stack.addWidget(HomeMenu())
        self.stack.addWidget(OrderForm())
        # form = HomeMenu()
        self.setCentralWidget(self.stack)

    def return_home(self):
        self.stack.setCurrentIndex(0)

    def next_page(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)
class HomeMenu(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        new_order_button = CPushButton("New Order", clicked=lambda: self.new_order_clicked())

        hbox.addStretch()
        hbox.addWidget(new_order_button)
        hbox.addStretch()
        vbox.addStretch()
        vbox.addLayout(hbox)
        vbox.addStretch()

        hbox2 = QHBoxLayout()
        hbox2.addStretch()

        settings_button = CPushButton("Settings", clicked=lambda: self.settings_clicked())
        settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        hbox2.addWidget(settings_button)

        vbox.addLayout(hbox2)

        self.settings = None


        self.setLayout(vbox)

    def new_order_clicked(self):
        self.parentWidget().parentWidget().next_page()

    def settings_clicked(self):
        self.settings = Settings()
        self.settings.show()
