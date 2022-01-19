import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Homepage import Homepage

import xlwt


def main():

    #Create App
    app = QApplication(sys.argv)

    #Set font
    _id = QtGui.QFontDatabase.addApplicationFont(resource_path("./fonts/Roboto/Roboto-Regular.ttf"))

    if QtGui.QFontDatabase.applicationFontFamilies(_id) == -1:
        print("problem loading font")
        sys.exit(-1)

    # Open the qss styles file and read in the css-alike styling code
    with open(resource_path("./data/style.qss"), 'r') as f:
        style = f.read()

        # Set the stylesheet of the application
        app.setStyleSheet(style)
    # print(QStyleFactory.keys())
    app.setStyle("Fusion")

    #Show Window
    win = Homepage()
    win.setGeometry(400, 400, 400, 300)

    win.show()
    sys.exit(app.exec_())


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    main()
