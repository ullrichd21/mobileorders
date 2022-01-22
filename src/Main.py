import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Homepage import Homepage
from tools import *

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
    # app.setStyle("Breeze")

    #Show Window
    win = Homepage()
    win.setGeometry(400, 400, 400, 300)

    win.show()
    sys.exit(app.exec_())




if __name__ == "__main__":
    main()
