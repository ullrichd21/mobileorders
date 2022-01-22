import threading

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import time

from cwidgets import CPushButton
import tools


class OrderForm(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.customer_data = {}
        self.order_data = {}

        # Create Layout
        self.layout = QVBoxLayout()

        # Create Stack
        self.stack = QStackedWidget()

        # Customer Form
        self.customer_form = CustomerForm(parent=self)

        # Order Details Form
        self.order_details_form = OrderDetailsForm()

        self.stack.addWidget(self.customer_form)
        self.stack.addWidget(self.order_details_form)

        # Add widgets
        self.layout.addWidget(self.stack)

        self.setLayout(self.layout)

    def submit_customer_data(self):
        self.layout.replaceWidget(self.next_button, self.submit_order_button)
        self.layout.replaceWidget(self.customer_form, self.order_details_form)
        # self.layout.replaceWidget()
        self.customer_form.deleteLater()
        self.next_button.deleteLater()

        self.stack.setCurrentIndex((self.stack.currentIndex() + 1) % self.stack.count())
        # self.customer_data = self.customer_form.get_customer_data()

    def next_page(self):
        print(str((self.stack.currentIndex() + 1) % self.stack.count()) + " " + str(self.stack.currentIndex()))

        self.stack.setCurrentIndex((self.stack.currentIndex() + 1) % self.stack.count())

    def submit_order(self):
        print({"customer_data": self.customer_data,
               "order_data": self.order_data})

        self.stack.setCurrentIndex(0)
        self.parentWidget().parentWidget().return_home()
        # return {"customer_data" : self.customer_form.get_customer_data(),
        #         "order_data" : self.order_details_form.get_order_data()}


class OrderDetailsForm(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        #Camera stuff
        self.camera = None
        self.popup = None
        self.viewfinder = None
        self.capture = None


        # Create a QFormLayout instance
        form_layout = QFormLayout()

        self.items = {"Dress": ["Small", "Regular", "Fluffy"],
                      "Corset": ["XXS", "XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"],
                      "Bodice": ["XXS", "XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"],
                      "Any Which Way": ["Regular", "Fluffy"],
                      "Long Skirt": ["Small", "Medium", "Large"],
                      "Peasant Top": ["Regular", "Fluffy"],
                      "Purse": ["One Size"],
                      "Repair": ["One Size"],
                      "Misc": ["One Size"]}

        # Add widgets to the layout
        self.item_input = QComboBox()
        self.item_input.addItems(self.items.keys())

        self.color_input = QLineEdit()

        self.item_details_input = QPlainTextEdit()
        self.size_input = QComboBox()  # Could also make this a dropdown that depends on the item selected.
        self.on_item_changed()
        self.item_input.currentIndexChanged.connect(lambda: self.on_item_changed())

        self.notes_input = QPlainTextEdit()

        # submit_button = QPushButton(
        #     "Submit", clicked=lambda: self.submit_clicked())
        # submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        form_layout.addRow("Item:", self.item_input)
        form_layout.addRow("Color:", self.color_input)
        form_layout.addRow("Item Details:", self.item_details_input)
        form_layout.addRow("Size:", self.size_input)
        form_layout.addRow("Additional Notes:", self.notes_input)
        form_layout.addRow(QLabel(""))
        self.attach_photo_button = CPushButton("Attach Photo", clicked=lambda: self.attach_photo_pressed())
        form_layout.addRow(QLabel(""))

        form_layout.addRow(self.attach_photo_button)
        # form_layout.addRow("Description:", self.description_input)
        # form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        # #Order label.
        # order_label = QLabel("Customer Info", alignment=Qt.AlignHCenter)
        #
        # outer_layout.addWidget(order_label)
        # outer_layout.addLayout(form_layout)
        # outer_layout.setAlignment(submit_button, Qt.AlignRight)
        # outer_layout.addStretch()
        #
        # center_layout.addLayout(outer_layout)
        # center_layout.addStretch()

        # Vbox Layout
        outer_layout = QVBoxLayout()

        # Order label.
        order_label = QLabel("Order Details", alignment=Qt.AlignHCenter)

        # Submit Order Button
        self.back_button = CPushButton("Back", clicked=lambda: self.go_back())
        self.submit_order_button = CPushButton("Submit Order", clicked=lambda: self.submit_order_data())

        outer_layout.addStretch()
        outer_layout.addWidget(order_label)
        outer_layout.addLayout(form_layout)
        outer_layout.addStretch()

        # Bottom Button
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.submit_order_button)

        outer_layout.addLayout(bottom_layout)
        # outer_layout.addWidget(self.submit_order_button, alignment=Qt.AlignRight)
        outer_layout.addStretch()

        # Horizontal Center
        hcenter = QHBoxLayout()
        hcenter.addStretch()
        hcenter.addLayout(outer_layout)
        hcenter.addStretch()

        # Create Layout
        self.setLayout(hcenter)

    def on_item_changed(self):
        self.size_input.clear()
        self.size_input.addItems(self.items[self.item_input.currentText()])

    def attach_photo_pressed(self):
        for camera_info in QCameraInfo.availableCameras():
            self.camera = QCamera(camera_info, self)
            if not self.camera.isCaptureModeSupported(QCamera.CaptureStillImage):
                print("Camera cannot capture images")
            break
        self.viewfinder = QCameraViewfinder()
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)

        self.camera.start()



        self.popup = QWidget()
        self.popup.setWindowTitle("Take a Photo")
        # self.popup.setGeometry(QRect(100, 100, 400, 200))

        hbox = QHBoxLayout()
        hbox.addStretch()

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.viewfinder)

        self.capture_button = CPushButton("Capture", clicked = lambda: self.capture_image())

        vbox.addWidget(self.capture_button)
        vbox.addStretch()
        hbox.addLayout(vbox)
        hbox.addStretch()

        self.popup.setLayout(hbox)
        self.viewfinder.show()
        self.popup.show()

    def capture_image(self):

        # time stamp
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")

        self.capture = QCameraImageCapture(self.camera)
        self.capture.capture(tools.resource_path("./photos/" + timestamp + ".jpg"))

    def submit_order_data(self):
        self.parentWidget().parentWidget().order_data = {"item": self.item_input.currentText(),
                                                         "item_details": self.item_details_input.toPlainText(),
                                                         "size": self.size_input.currentText(),
                                                         "notes": self.notes_input.toPlainText()}


        self.clear_order_data()
        self.parentWidget().parentWidget().customer_form.clear_customer_data()

        self.parentWidget().parentWidget().submit_order()

    def clear_order_data(self):
        self.item_input.setCurrentIndex(0)
        self.item_details_input.setPlainText("")
        self.size_input.setCurrentIndex(0)
        self.notes_input.setPlainText("")

    def go_back(self):
        # print(str((self.stack.currentIndex() + 1) % self.stack.count()) + " " + str(self.stack.currentIndex()))

        self.parentWidget().parentWidget().stack.setCurrentIndex((self.parentWidget().parentWidget().stack.currentIndex() - 1) % self.parentWidget().parentWidget().stack.count())

class CustomerForm(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        # Create a QFormLayout instance
        form_layout = QFormLayout()

        # Add widgets to the layout
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.phone_number_input = QLineEdit()
        self.email_input = QLineEdit()

        self.regEx = QRegExpValidator(QRegExp("[0-9]*"))
        self.phone_number_input.setValidator(self.regEx)

        # Address input
        self.address_input = QLineEdit()
        self.address_apartment_input = QLineEdit()
        self.address_city_input = QLineEdit()
        self.address_state_input = QComboBox()
        self.address_state_input.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.address_state_input.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.address_state_input.setMaxVisibleItems(10)
        # self.address_state_input.setContentsMargins(5,5,5,5)
        # self.address_state_input.setEditable(True)
        # self.address_state_input.lineEdit().setReadOnly(True)
        # self.address_state_input.lineEdit().setDisabled(True)
        # self.address_state_input.lineEdit().setAlignment(Qt.AlignCenter)
        # self.address_state_input.setEditable(False)
        self.address_country_input = QComboBox()
        self.address_country_input.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.address_country_input.setMaxVisibleItems(10)
        self.address_country_input.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.address_country_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.address_zip_input = QLineEdit()

        self.address_zip_input.setValidator(self.regEx)

        with open(tools.resource_path("./data/states.txt")) as states, open(
                tools.resource_path("./data/countries.txt")) as countries:
            self.address_state_input.addItems(states.readlines())
            self.address_country_input.addItems(countries.readlines())

        # submit_button = QPushButton(
        #     "Submit", clicked=lambda: self.submit_clicked())
        # submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        spacer = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_number_input)
        form_layout.addRow("Address:", self.address_input)
        form_layout.addRow("Apartment, Suite, etc:", self.address_apartment_input)
        form_layout.addRow("City:", self.address_city_input)
        form_layout.addRow("State:", self.address_state_input)
        form_layout.addRow("Country:", self.address_country_input)
        form_layout.addRow("Zip / Postal Code:", self.address_zip_input)
        # form_layout.addRow("Description:", self.description_input)
        # form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        form_layout.setVerticalSpacing(10)

        # Vbox Layout
        outer_layout = QVBoxLayout()

        # Order label.
        order_label = QLabel("Customer Info", alignment=Qt.AlignHCenter)

        # Next Button
        self.next_button = CPushButton("Next", clicked=lambda: self.submit_customer_data())

        # Add Widgets
        outer_layout.addStretch()
        outer_layout.addWidget(order_label)
        outer_layout.addLayout(form_layout)
        outer_layout.addStretch()

        # LastRow
        bottom_accept = QHBoxLayout()
        bottom_accept.addStretch()
        bottom_accept.addWidget(self.next_button)
        outer_layout.addLayout(bottom_accept)
        # outer_layout.addWidget(self.next_button, alignment=Qt.AlignRight)
        outer_layout.addStretch()
        # Horizontal Center
        hcenter = QHBoxLayout()
        hcenter.addStretch()
        hcenter.addLayout(outer_layout)
        hcenter.addStretch()
        #
        # outer_layout.addWidget(order_label)
        # outer_layout.addLayout(form_layout)
        # outer_layout.setAlignment(submit_button, Qt.AlignRight)
        # outer_layout.addStretch()
        #
        # center_layout.addLayout(outer_layout)
        # center_layout.addStretch()

        # Create Layout
        self.setLayout(hcenter)

    def submit_customer_data(self):
        self.parentWidget().parentWidget().customer_data = {"first_name": self.first_name_input.text(),
                                                            "last_name": self.last_name_input.text(),
                                                            "email": self.email_input.text(),
                                                            "phone_number": self.phone_number_input.text(),
                                                            "address": self.address_input.text(),
                                                            "apartment": self.address_apartment_input.text(),
                                                            "city": self.address_city_input.text(),
                                                            "state": self.address_state_input.currentText(),
                                                            "country": self.address_country_input.currentText(),
                                                            "zip": self.address_zip_input.text(),
                                                            }
        self.parentWidget().parentWidget().next_page()

    def clear_customer_data(self):
        self.first_name_input.setText("")
        self.last_name_input.setText("")
        self.email_input.setText("")
        self.phone_number_input.setText("")
        self.address_input.setText("")
        self.address_apartment_input.setText("")
        self.address_city_input.setText("")
        self.address_state_input.setCurrentIndex(0)
        self.address_country_input.setCurrentIndex(0)
        self.address_zip_input.setText("")
