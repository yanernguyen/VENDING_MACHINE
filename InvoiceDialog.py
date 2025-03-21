import os
import webbrowser

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class InvoiceDialog(QDialog):
    def __init__(self, invoice, parent=None):
        super().__init__(parent)
        self.invoice = invoice
        self.pdf_path = None
        self.payment_method = None  # Lưu phương thức thanh toán

        self.setWindowTitle("Hóa đơn thanh toán")
        self.setFixedSize(500, 600)

        layout = QVBoxLayout()
        self.label_total = QLabel(f"Tổng tiền: {invoice.total:,.0f}đ")
        self.label_tax = QLabel(f"Thuế: {invoice.tax:,.0f}đ")
        self.label_final_total = QLabel(f"Tổng tiền sau thuế: {invoice.total_after_tax:,.0f}đ")

        layout.addWidget(self.label_total)
        layout.addWidget(self.label_tax)
        layout.addWidget(self.label_final_total)

        invoice_data = invoice.to_dict()


        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Sản phẩm", "Số lượng", "Giá", "Tổng"])
        self.table.setRowCount(len(invoice_data["cart"]))

        for row, item in enumerate(invoice_data["cart"]):
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["qty"])))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['unit_price']:,.0f}đ"))
            self.table.setItem(row, 3,
                               QTableWidgetItem(f"{item.get('total_price', item['qty'] * item['unit_price']):,.0f}đ"))

        layout.addWidget(self.table)

        self.btn_momo = QPushButton("Chuyển khoản")
        self.btn_momo.clicked.connect(lambda: self.process_payment("MoMo"))

        self.btn_credit = QPushButton("Thẻ tín dụng")
        self.btn_credit.clicked.connect(lambda: self.process_payment("Thẻ tín dụng"))

        self.btn_cash = QPushButton("Tiền mặt")
        self.btn_cash.clicked.connect(lambda: self.process_payment("Tiền mặt"))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_momo)
        button_layout.addWidget(self.btn_credit)
        button_layout.addWidget(self.btn_cash)
        layout.addLayout(button_layout)


        self.btn_download_pdf = QPushButton("Tải hóa đơn (PDF)")
        self.btn_download_pdf.setEnabled(False)
        self.btn_download_pdf.clicked.connect(self.generate_invoice)
        layout.addWidget(self.btn_download_pdf)


        self.btn_view_invoice = QPushButton("Xem hóa đơn")
        self.btn_view_invoice.setEnabled(False)
        self.btn_complete = QPushButton("Hoàn thành")
        self.btn_complete.clicked.connect(self.complete_transaction)
        layout.addWidget(self.btn_complete)


        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qr_label)

        self.setLayout(layout)

    def process_payment(self, method):
        self.payment_method = method
        QMessageBox.information(self, "Phương thức thanh toán", f"Bạn đã chọn: {method}")

        if method == "MoMo":
            self.show_momo_qr()
        elif method == "Thẻ tín dụng":
            webbrowser.open("https://www.paypal.com/")


        self.btn_download_pdf.setEnabled(True)

    def generate_invoice(self):
        if not self.payment_method:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn phương thức thanh toán trước!")
            return

        self.invoice.generate_invoice()


        invoices_folder = os.path.join(os.getcwd(), "Invoices")
        files = sorted(os.listdir(invoices_folder), reverse=True)
        if files:
            self.pdf_path = os.path.join(invoices_folder, files[0])
            QMessageBox.information(self, "Hoàn tất", "Hóa đơn PDF đã được tạo thành công!")

    def complete_transaction(self):
        QMessageBox.information(self, "Hoàn tất", "Thanh toán đã hoàn thành. Cảm ơn bạn!")
        self.accept()

    def show_momo_qr(self):
        pixmap = QPixmap("qr/momo_qr.JPG")
        self.qr_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
