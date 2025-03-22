from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLabel, QFrame, QPushButton, QVBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
import sys
from CInvoice import Invoice
from CProductList import ProductList
from CCart import Cart

from InvoiceDialog import InvoiceDialog



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('giaodien2.ui', self)

        self.productlist = ProductList()
        self.cart = Cart()

        self.selected_frames = []
        self.cart_table = self.findChild(QtWidgets.QTableWidget, "cart_table")
        self.label_total = self.findChild(QtWidgets.QLabel, "label_total")
        self.search_bar = self.findChild(QtWidgets.QLineEdit, "search_bar")
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, "scrollArea_products")
        self.scrollContent2 = self.scroll_area.widget()
        self.product_container = self.scrollContent2.findChild(QtWidgets.QGridLayout, "productContainer")
        self.scroll_area.setWidgetResizable(True)
        self.scrollContent2.adjustSize()
        self.pushButton_icon = self.findChild(QtWidgets.QPushButton, "pushButton_icon")
        print(self.pushButton_icon)
        icon = QIcon("image/icon.jpg")
        self.pushButton_icon.setIcon(icon)
        self.pushButton_icon.setIconSize(QSize(30, 30))

        self.scroll_area.widget().adjustSize()
        self.current_category = "Beverages"
        self.lienketnutlenh()
        self.setup_products()
        self.show()


    def lienketnutlenh(self):

        self.pushButton_SEARCH.clicked.connect(self.search_product)
        self.pushButton_ADD.clicked.connect(self.add_to_cart)
        self.pushButton_REMOVE.clicked.connect(self.remove_from_cart)
        self.pushButton_CHECKOUT.clicked.connect(self.checkout)
        self.pushButton_icon.clicked.connect(self.open_login_window)
        self.pushButton_ADD_2.clicked.connect(self.cancle)
        self.pushButton_icon.clicked.connect(self.open_login_window)


        self.pushButton_Beverages.clicked.connect(lambda: self.filter_product("Beverages"))
        self.pushButton_FastFood.clicked.connect(lambda: self.filter_product("Fast Food"))
        self.pushButton_Snacks.clicked.connect(lambda: self.filter_product("Snacks"))
        self.pushButton_PersonalCares.clicked.connect(lambda: self.filter_product("Personal Cares"))

    def open_login_window(self):
        from xulygiaodienlogin import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()


    def setup_products(self):
        self.scroll_widget = QtWidgets.QWidget()
        self.product_container = QtWidgets.QGridLayout(self.scroll_widget) # Sử dụng layout dọc thay vì grid
        self.product_container.setSpacing(10)
        self.scroll_area.setWidget(self.scroll_widget)  # Đặt widget cuộn
        self.scroll_area.setWidgetResizable(True)
        self.load_products()


    def load_products(self):
        self.products = self.productlist.products
        self.filter_product("Beverages")

    def add_product(self, product, row, col):
        product_frame = QFrame()
        product_frame.setLayout(QVBoxLayout())
        product_frame.setFixedSize(200, 241)

        label_image = QLabel()
        pixmap = QPixmap(product.image)
        if not pixmap.isNull():

            label_image.setPixmap(pixmap)
        else:
            label_image.setText("No Image")
        label_image.setScaledContents(True)


        button = QPushButton(f"{product.name}\nPrice: {product.price:,}đ | Stock: {product.stock}")
        button.clicked.connect(lambda checked, frame=product_frame: self.hightlight(frame))
        button.product_data = product
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #AFE1AF;
                color: black;
                font-size: 12px;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                border: 1px solid #4CAF50;
                color: #388E3C;
            }
            QPushButton:pressed {
                border: 2px solid #1B5E20;
                color: #1B5E20;
            }
        """)


        product_frame.layout().addWidget(label_image)
        product_frame.layout().addWidget(button)


        self.product_container.addWidget(product_frame, row, col)

    def add_to_cart(self):

        if not self.selected_frames:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm để thêm vào giỏ hàng.")
            return


        for selected_frame in self.selected_frames:
            button = selected_frame.findChild(QPushButton)
            if button and hasattr(button, "product_data"):
                product = button.product_data
                if not self.cart.add_product(product.id):
                    QMessageBox.warning(self, "Lỗi",
                                        f"Không thể thêm sản phẩm '{product.name}' vào giỏ hàng. Có thể số lượng tồn kho không đủ.")



        self.update_cart_table()
        self.selected_frames.clear()
        self.update_total_price()

        self.filter_product(self.current_category)

    def update_total_price(self):
        sub_total, tax, total  = self.cart.get_total()
        self.label_subtotal.setText(f"{sub_total:,.0f}đ")
        self.label_tax.setText(f"{tax:,.0f}đ")
        self.label_total.setText(f"{total:,.0f}đ")


    def update_cart_table(self):
        self.cart_table.setRowCount(0)
        self.label_subtotal.clear()
        self.label_total.clear()
        self.label_tax.clear()
        for row, item in enumerate(self.cart.to_dict()):
            product_id = item.get('product_id')
            if not product_id:
                continue
            product = self.productlist.get_product_by_id(product_id)
            if product:
                self.cart_table.insertRow(row)
                self.cart_table.setItem(row, 0, QTableWidgetItem(product.name))
                self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['qty'])))
                product_total = item['qty'] * product.price
                self.cart_table.setItem(row, 2, QTableWidgetItem(f"{product_total:,.0f}đ"))
        self.cart_table.verticalHeader().setVisible(False)

    def search_product(self):

        search_text = self.search_bar.text().lower()


        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()


        row, col = 0, 0
        for product in self.productlist.products:
            if search_text in product.name.lower():
                self.add_product(product, row, col)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1

    def hightlight(self, selected_frame):
        if selected_frame in self.selected_frames:
            self.selected_frames.remove(selected_frame)
            selected_frame.setStyleSheet("QFrame { border: none; }")
        else:

            self.selected_frames.append(selected_frame)
            selected_frame.setStyleSheet("""
                            QFrame {
                                border: 2px solid #A3D9A5;  /* Viền xanh nhạt */
                                border-radius: 6px;
                            }
                            QLabel, QPushButton {
                                border: none;  /* Đảm bảo QLabel và QPushButton không bị viền */
                                background: transparent;
                            }
                        """)

    def remove_from_cart(self):

        if self.cart_table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống.")
            return

        selected_row = self.cart_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm trong giỏ hàng.")
            return

        product_name_item = self.cart_table.item(selected_row, 0)
        if not product_name_item:
            QMessageBox.warning(self, "Error", "Không thể xác định sản phẩm được chọn.")
            return

        product_name = product_name_item.text()


        product_to_remove = None
        for item in self.cart.to_dict():
            product_id = item.get('product_id')
            if not product_id:
                continue
            product = self.productlist.get_product_by_id(product_id)
            if product and product.name == product_name:
                product_to_remove = product
                self.product_list.save_products()
                break

        if not product_to_remove:
            QMessageBox.warning(self, "Error", "Không tìm thấy sản phẩm trong giỏ hàng.")
            return


        self.cart.remove_product(product_to_remove.id)
        self.update_cart_table()
        QMessageBox.information(self, "Success", f"Sản phẩm '{product_name}' đã được xóa khỏi giỏ hàng.")

    def checkout(self):
        total, tax, total_after_tax = self.cart.checkout()

        if total == -1:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống.")
        else:
            invoice = Invoice(self.cart.to_dict(), total,tax, total_after_tax)

            invoice.save_to_json()

            for item in self.cart.to_dict():
                product_id = item['product_id']
                quantity = item['qty']
                success = self.productlist.reduce_stock(product_id, quantity)
                if success is False:
                    QMessageBox.warning(self, "Lỗi", f"Sản phẩm {item['product_id']} không đủ hàng.")

            self.productlist.save_products()
            self.load_products()
            dialog = InvoiceDialog(invoice, self)
            dialog.exec()
            self.cart.clear()
            self.label_subtotal.setText(f" {invoice.total:,.0f}đ")
            self.label_tax.setText(f" {invoice.tax:,.0f}đ")
            self.label_total.setText(f" {invoice.total_after_tax:,.0f}đ")

            self.update_cart_table()

    def cancle(self):
        self.cart.clear()
        self.update_cart_table()


    def filter_product(self, category="Beverages"):

        self.current_category = category

        if hasattr(self, "selected_frames"):
            self.selected_frames.clear()

        filtered_products = [p for p in self.productlist.products if p.category == category]

        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        row, col = 0, 0
        for product in filtered_products:
            self.add_product(product, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        self.scroll_widget.adjustSize()
        self.scroll_area.verticalScrollBar().setValue



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
