from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import uic
from CProductList import ProductList

class ManagerWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        uic.loadUi("manage.ui", self)
        self.setWindowTitle(f"Quản lý sản phẩm - {username}")

        self.product_list = ProductList()
        self.admin_name = username  # Lưu tên admin
        self.dinhnghianutlenh()
        self.load_products()

    def dinhnghianutlenh(self):
        self.pushButton_update.clicked.connect(self.update_stock)


    def load_products(self):
        self.tableWidget.setRowCount(len(self.product_list.products))
        for row, product in enumerate(self.product_list.products):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(product.id))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(product.name))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(product.category))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(product.price)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(product.stock)))

    def update_stock(self):
        product_id = self.lineEdit_ID.text()
        quantity = self.lineEdit_SL.text()

        if not product_id or not quantity.isdigit():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã sản phẩm và số lượng hợp lệ!")
            return

        success = self.product_list.update_product_stock(product_id, int(quantity), self.admin_name)
        if success:
            QMessageBox.information(self, "Thành công", "Cập nhật số lượng thành công!")
            self.load_products()
        else:
            QMessageBox.warning(self, "Lỗi", "Mã sản phẩm không tồn tại!")
