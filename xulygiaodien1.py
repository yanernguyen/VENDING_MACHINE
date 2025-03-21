from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QLabel, QFrame, QPushButton, QVBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
from Function import *  # Import class quản lý sản phẩm và giỏ hàng

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('giaodien.ui', self)
        # Khởi tạo các biến và tham chiếu UI
        self.functions = SmartMartFunctions()  # Class quản lý sản phẩm và giỏ hàng
        self.selected_frames = []  # Danh sách các sản phẩm được chọn
        self.cart_table = self.findChild(QtWidgets.QTableWidget, "cart_table")
        self.label_total = self.findChild(QtWidgets.QLabel, "label_total")
        self.search_bar = self.findChild(QtWidgets.QLineEdit, "search_bar")
        self.scroll_area = self.findChild(QtWidgets.QScrollArea, "scrollArea_products")
        self.product_container = self.findChild(QtWidgets.QGridLayout, "productContainer")

        self.lienketnutlenh()
        self.setup_products()
        self.show()

    def lienketnutlenh(self):
        # Kết nối các nút với hàm xử lý
        self.pushButton_SEARCH.clicked.connect(self.search_product)
        self.pushButton_ADD.clicked.connect(self.add_to_cart)
        self.pushButton_REMOVE.clicked.connect(self.remove_from_cart)
        self.pushButton_CHECKOUT.clicked.connect(self.checkout)

        # Kết nối các nút danh mục với filter_product
        self.pushButton_Beverages.clicked.connect(lambda: self.filter_product("Beverages"))
        self.pushButton_FastFood.clicked.connect(lambda: self.filter_product("Fast Food"))
        self.pushButton_Snacks.clicked.connect(lambda: self.filter_product("Snacks"))
        self.pushButton_PersonalCares.clicked.connect(lambda: self.filter_product("Personal Cares"))

    def setup_products(self):
        # Thiết lập giao diện sản phẩm ban đầu
        self.product_container.setSpacing(10)  # Giãn cách giữa các sản phẩm
        self.load_products()

    def load_products(self):
        # Lấy danh sách sản phẩm từ SmartMartFunctions
        self.products = self.functions.products

        # Hiển thị danh mục mặc định (ví dụ: "Beverages")
        self.filter_product("Beverages")

    def add_product(self, product, row, col):
        # Tạo frame sản phẩm
        product_frame = QFrame()
        product_frame.setLayout(QVBoxLayout())

        # Hiển thị ảnh sản phẩm
        label_image = QLabel()
        pixmap = QPixmap(product.image)  # Đường dẫn ảnh từ JSON
        if not pixmap.isNull():
            label_image.setPixmap(pixmap)
        else:
            label_image.setText("No Image")  # Nếu không tìm thấy hình ảnh
        label_image.setScaledContents(True)

        # Hiển thị thông tin sản phẩm
        button = QPushButton(f"{product.name}\n{product.price:,}đ\nStock: {product.stock}")
        button.clicked.connect(lambda checked, frame=product_frame: self.hightlight(frame))
        button.product_data = product  # Lưu đối tượng sản phẩm vào nút (sửa đổi)

        # Thêm các widget vào frame sản phẩm
        product_frame.layout().addWidget(label_image)
        product_frame.layout().addWidget(button)

        # Thêm frame sản phẩm vào container
        self.product_container.addWidget(product_frame, row, col)

    def add_to_cart(self):
        # Lấy sản phẩm được chọn từ danh sách highlight
        if not self.selected_frames:
            QMessageBox.warning(self, "Error", "Vui lòng chọn một sản phẩm để thêm vào giỏ hàng.")
            return

        # Duyệt qua từng frame sản phẩm được chọn
        for selected_frame in self.selected_frames:
            button = selected_frame.findChild(QPushButton)
            if button and hasattr(button, "product_data"):
                product = button.product_data  # Lấy đối tượng sản phẩm từ nút

                # Kiểm tra số lượng tồn kho trước khi thêm vào giỏ hàng
                if product.stock <= 0:
                    QMessageBox.warning(self, "Error", f"Sản phẩm '{product.name}' đã hết hàng.")
                    continue  # Bỏ qua sản phẩm này nếu hết hàng

                # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
                if self.functions.cart.has_item(product.id):  # Nếu đã có trong giỏ hàng
                    self.functions.cart.update_item_quantity(product.id, 1)  # Tăng số lượng lên 1
                else:  # Nếu chưa có trong giỏ hàng
                    if not self.functions.add_to_cart(product.id):  # Thêm sản phẩm mới vào giỏ hàng
                        QMessageBox.warning(self, "Error", f"Không thể thêm sản phẩm '{product.name}' vào giỏ hàng.")
                        continue  # Bỏ qua sản phẩm này nếu không thể thêm

                # Giảm số lượng stock của sản phẩm
                product.stock -= 1  # Giảm số lượng tồn kho
                if product.stock < 0:
                    product.stock = 0  # Đảm bảo stock không âm

        # Cập nhật lại bảng giỏ hàng sau khi xử lý tất cả sản phẩm
        self.update_cart_table()
        self.load_products()
        # 🔥 Cập nhật tổng giá ngay lập tức     #nè mới them
        self.update_total_price()
        # Xóa danh sách sản phẩm được chọn sau khi thêm vào giỏ hàng
        self.selected_frames.clear()

    def update_total_price(self):     #voi này mới them
        """Cập nhật tổng giá tiền của giỏ hàng ngay lập tức."""
        total_price = self.functions.cart.get_total()  # Lấy tổng giá từ giỏ hàng
        self.label_total.setText(f"{total_price:,.0f}đ")  # Cập nhật giao diện

    def update_cart_table(self):
        self.cart_table.setRowCount(0)  # Xóa tất cả các dòng hiện tại
        for row, item in enumerate(self.functions.cart.to_dict()):  # Duyệt qua từng mục trong giỏ hàng
            product = self.functions.get_product_by_id(item['product_id'])  # Tìm sản phẩm bằng product_id
            if product:
                self.cart_table.insertRow(row)
                # Tên sản phẩm
                self.cart_table.setItem(row, 0, QTableWidgetItem(product.name))
                # Số lượng
                self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['qty'])))  # Chuyển số lượng thành chuỗi
                # Giá
                self.cart_table.setItem(row, 2, QTableWidgetItem(f"{product.price:,}đ"))

    def search_product(self):
        # Tìm kiếm sản phẩm theo từ khóa
        search_text = self.search_bar.text().lower()

        # Xóa các widget cũ
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Hiển thị sản phẩm phù hợp với từ khóa tìm kiếm
        row, col = 0, 0
        for product in self.functions.products:
            if search_text in product.name.lower():
                self.add_product(product, row, col)
                col += 1
                if col >= 3:  # 3 cột mỗi hàng
                    col = 0
                    row += 1

    def hightlight(self, selected_frame):
        # Highlight sản phẩm khi được chọn
        if selected_frame in self.selected_frames:
            # Nếu frame đã được chọn, bỏ chọn nó
            self.selected_frames.remove(selected_frame)
            selected_frame.setStyleSheet("QFrame { border: none; }")
        else:
            # Nếu frame chưa được chọn, thêm vào danh sách chọn
            self.selected_frames.append(selected_frame)
            selected_frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #ADD8E6;  /* Viền xanh nhạt */
                    border-radius: 4px;
                }
                QLabel, QPushButton {
                    border: none;  /* Đảm bảo QLabel và QPushButton không bị viền */
                    background: transparent;
                }
            """)

    def remove_from_cart(self):
        # Kiểm tra xem giỏ hàng có trống không
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
        product_name = product_name_item.text()  # Lấy tên sản phẩm
        product_to_remove = None
        for item in self.functions.cart.to_dict():
            product = self.functions.get_product_by_id(item['product_id'])
            if product and product.name == product_name:
                product_to_remove = product
                break
        if not product_to_remove:
            QMessageBox.warning(self, "Error", "Không tìm thấy sản phẩm trong giỏ hàng.")
            return
        qty_in_cart = item['qty']
        self.functions.cart.remove_item(product_to_remove.id)
        product_to_remove.stock += qty_in_cart
        self.update_cart_table()
        # Cập nhật lại danh sách sản phẩm hiển thị
        self.load_products()
        QMessageBox.information(self, "Success", f"Sản phẩm '{product_name}' đã được xóa khỏi giỏ hàng.")

    def checkout(self):
        # Gọi hàm checkout từ đối tượng SmartMartFunctions
        total = self.functions.checkout()
        if total == 0:
            QMessageBox.warning(self, "Error", "Giỏ hàng đang trống hoặc thanh toán không thành công.")
        else:
            self.label_total.setText(f"{total:,.0f}đ")  #Mới bỏ chữ tổng tiền
            QMessageBox.information(self, "Checkout", f"Tổng tiền: {total:,}đ\nThanh toán thành công!")
            self.update_cart_table()  # Cập nhật lại bảng giỏ hàng

    def filter_product(self, category):
        if hasattr(self, "selected_frames"):
            self.selected_frames.clear()
        # Lọc sản phẩm theo category
        filtered_products = [p for p in self.functions.products if p.category == category]
        # Xóa widget cũ
        for i in reversed(range(self.product_container.count())):
            widget = self.product_container.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        # Hiển thị sản phẩm mới
        row, col = 0, 0
        for product in filtered_products:
            self.add_product(product, row, col)
            col = (col + 1) % 3  # 3 cột/hàng
            row += 1 if col == 0 else 0


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
