import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QSplitter,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from funtion import SmartMartFunctions


class SmartMartUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartMart Kiosk")
        self.setGeometry(100, 100, 1000, 600)

        # Initialize functions
        self.functions = SmartMartFunctions()

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        # Splitter to divide the window into left (menu) and right (cart)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout.addWidget(self.splitter)

        # Left side: Menu
        self.menu_frame = QFrame()
        self.menu_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.menu_layout = QVBoxLayout(self.menu_frame)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search products...")
        self.search_bar.setStyleSheet("padding: 10px; font-size: 16px;")
        self.search_bar.textChanged.connect(self.search_product)
        self.menu_layout.addWidget(self.search_bar)

        # Product categories (hardcoded for simplicity)
        self.categories = ["Beverages", "Fast Food", "Snacks", "Personal Care"]
        self.category_buttons = []
        for category in self.categories:
            button = QPushButton(category)
            button.setStyleSheet(
                """
                QPushButton {
                    padding: 15px;
                    font-size: 18px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                """
            )
            button.clicked.connect(lambda _, cat=category: self.show_category_products(cat))
            self.menu_layout.addWidget(button)

        # Product list
        self.product_list = QListWidget()
        self.product_list.setStyleSheet("font-size: 16px;")
        self.menu_layout.addWidget(self.product_list)

        # Add to cart button
        self.add_to_cart_button = QPushButton("Add to Cart")
        self.add_to_cart_button.setStyleSheet(
            """
            QPushButton {
                padding: 15px;
                font-size: 18px;
                background-color: #008CBA;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #007B9E;
            }
            """
        )
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        self.menu_layout.addWidget(self.add_to_cart_button)

        # Add menu frame to splitter
        self.splitter.addWidget(self.menu_frame)

        # Right side: Cart
        self.cart_frame = QFrame()
        self.cart_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cart_layout = QVBoxLayout(self.cart_frame)

        # Cart title
        self.cart_title = QLabel("Your Cart")
        self.cart_title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.cart_title.setStyleSheet("color: #333;")
        self.cart_layout.addWidget(self.cart_title)

        # Cart list
        self.cart_list = QListWidget()
        self.cart_list.setStyleSheet("font-size: 16px;")
        self.cart_layout.addWidget(self.cart_list)

        # Total label
        self.total_label = QLabel("Total: $0.00")
        self.total_label.setFont(QFont("Arial", 20))
        self.total_label.setStyleSheet("color: #333;")
        self.cart_layout.addWidget(self.total_label)

        # Remove from cart button
        self.remove_from_cart_button = QPushButton("Remove from Cart")
        self.remove_from_cart_button.setStyleSheet(
            """
            QPushButton {
                padding: 15px;
                font-size: 18px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            """
        )
        self.remove_from_cart_button.clicked.connect(self.remove_from_cart)
        self.cart_layout.addWidget(self.remove_from_cart_button)

        # Checkout button
        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.setStyleSheet(
            """
            QPushButton {
                padding: 15px;
                font-size: 18px;
                background-color: #555;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            """
        )
        self.checkout_button.clicked.connect(self.checkout)
        self.cart_layout.addWidget(self.checkout_button)

        # Add cart frame to splitter
        self.splitter.addWidget(self.cart_frame)

        # Initialize product list
        self.show_category_products(self.categories[0])

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


def main():
    app = QApplication(sys.argv)
    window = SmartMartUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()