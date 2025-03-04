from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
import sys
from funtion import *

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('giaodien.ui', self)
        self.lienketnutlenh()
        self.functions = SmartMartFunctions()
        self.show()
    def lienketnutlenh(self):
        self.pushButton_SEARCH.clicked.connect(self.search_product)
        self.pushButton_ADD.clicked.connect(self.add_to_cart)
        self.pushButton_REMOVE.clicked.connect(self.remove_from_cart)
        self.pushButton_CHECKOUT.clicked.connect(self.checkout)
    def show_category_products(self, category):
        self.product_list.clear()
        for product in self.functions.products:
            if product.category == category:
                self.product_list.addItem(str(product))

    def update_cart_list(self):
        self.cart_list.clear()
        for product_name, quantity in self.functions.cart.items.items():
            self.cart_list.addItem(f"{product_name} x {quantity}")
        self.total_label.setText(f"Total: ${self.functions.cart.get_total(self.functions.products):.2f}")

    def search_product(self):
        search_text = self.search_bar.text().lower()
        self.product_list.clear()
        for product in self.functions.search_products(search_text):
            self.product_list.addItem(str(product))

    def add_to_cart(self):
        selected_item = self.product_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select a product.")
            return

        product_name = selected_item.text().split(" ")[0]
        if self.functions.add_to_cart(product_name):
            self.update_cart_list()
        else:
            QMessageBox.warning(self, "Error", "Product out of stock.")

    def remove_from_cart(self):
        selected_item = self.cart_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select an item from the cart.")
            return

        product_name = selected_item.text().split(" ")[0]
        if self.functions.remove_from_cart(product_name):
            self.update_cart_list()

    def checkout(self):
        total = self.functions.checkout()
        QMessageBox.information(self, "Checkout", f"Total: ${total:.2f}\nPayment successful! Dispensing your items.")
        self.update_cart_list()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.lienketnutlenh()
app.exec()
