from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class OrderForm(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.customer_data = {}
        self.order_data = {}

        #Create Layout
        self.layout = QVBoxLayout()

        #Create Stack
        self.stack = QStackedWidget()

        #Customer Form
        self.customer_form = CustomerForm(parent=self)

        #Order Details Form
        self.order_details_form = OrderDetailsForm()

        self.stack.addWidget(self.customer_form)
        self.stack.addWidget(self.order_details_form)

        #Add widgets
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
        print({"customer_data" : self.customer_data,
                "order_data" : self.order_data})


        self.stack.setCurrentIndex(0)
        self.parentWidget().parentWidget().return_home()
        # return {"customer_data" : self.customer_form.get_customer_data(),
        #         "order_data" : self.order_details_form.get_order_data()}

class OrderDetailsForm(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        # Create a QFormLayout instance
        form_layout = QFormLayout()

        items = ["Dress",
                "Corset",
                "Bodice",
                "Any Which Way",
                "Long Skirt",
                "Peasant Top",
                "Purse",
                "Repair",
                "Misc"]

        # Add widgets to the layout
        self.item_input = QComboBox()
        self.item_input.addItems(items)

        self.item_details_input = QPlainTextEdit()
        self.size_input = QLineEdit() #Could also make this a dropdown that depends on the item selected.

        self.notes_input = QPlainTextEdit()

        # submit_button = QPushButton(
        #     "Submit", clicked=lambda: self.submit_clicked())
        # submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        form_layout.addRow("Item:", self.item_input)
        form_layout.addRow("Item Details:", self.item_details_input)
        form_layout.addRow("Size:", self.size_input)
        form_layout.addRow("Additional Notes:", self.notes_input)
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

        #Vbox Layout
        outer_layout = QVBoxLayout()

        #Order label.
        order_label = QLabel("Order Details", alignment=Qt.AlignHCenter)

        #Submit Order Button
        self.submit_order_button = QPushButton("Submit Order", clicked = lambda: self.submit_order_data())

        outer_layout.addWidget(order_label)
        outer_layout.addLayout(form_layout)
        outer_layout.addStretch()
        outer_layout.addWidget(self.submit_order_button, alignment=Qt.AlignRight)

        #Create Layout
        self.setLayout(outer_layout)

    def submit_order_data(self):
        self.parentWidget().parentWidget().order_data = {"item" : self.item_input.currentText(),
                "item_details" : self.item_details_input.toPlainText(),
                "size" : self.size_input.text(),
                "notes" : self.notes_input.toPlainText()}

        self.item_input.setCurrentIndex(0)
        self.item_details_input.setPlainText("")
        self.size_input.setText("")
        self.notes_input.setPlainText("")

        self.parentWidget().parentWidget().submit_order()

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

        self.address_input = QLineEdit()

        # submit_button = QPushButton(
        #     "Submit", clicked=lambda: self.submit_clicked())
        # submit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone Number:", self.phone_number_input)
        form_layout.addRow("Address:", self.address_input)
        # form_layout.addRow("Description:", self.description_input)
        # form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        #Vbox Layout
        outer_layout = QVBoxLayout()

        #Order label.
        order_label = QLabel("Customer Info", alignment=Qt.AlignHCenter)

        #Next Button
        self.next_button = QPushButton("Next", clicked = lambda: self.submit_customer_data())

        #Add Widgets
        outer_layout.addWidget(order_label)
        outer_layout.addLayout(form_layout)
        outer_layout.addStretch()
        outer_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        #
        # outer_layout.addWidget(order_label)
        # outer_layout.addLayout(form_layout)
        # outer_layout.setAlignment(submit_button, Qt.AlignRight)
        # outer_layout.addStretch()
        #
        # center_layout.addLayout(outer_layout)
        # center_layout.addStretch()

        #Create Layout
        self.setLayout(outer_layout)

    def submit_customer_data(self):
        self.parentWidget().parentWidget().customer_data = {"first_name" : self.first_name_input.text(),
                "last_name" : self.last_name_input.text(),
                "email" : self.email_input.text(),
                "phone_number" : self.phone_number_input.text(),
                "address" : self.address_input.text()}

        self.first_name_input.setText("")
        self.last_name_input.setText("")
        self.email_input.setText("")
        self.phone_number_input.setText("")
        self.address_input.setText("")

        self.parentWidget().parentWidget().next_page()
