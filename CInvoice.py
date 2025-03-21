import json
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from CCart import Cart
import time
import os

import os
DATA_PATH = os.path.join("data", "invoices.json")
class Invoice:
    def __init__(self, cart: Cart, total: float, tax:float, total_after_tax:float):
        self.cart = cart
        self.total = total
        self.tax = tax
        self.total_after_tax = total_after_tax
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "cart": self.cart.to_dict() if isinstance(self.cart, Cart) else self.cart,
            "datetime": self.datetime,
            "total": self.total,
            "tax": self.tax,
            "total_after_tax":self.total_after_tax
        }

    def save_to_json(self):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                invoices = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            invoices = []

        invoices.append(self.to_dict())

        with open(DATA_PATH, "w", encoding="utf-8") as file:
            json.dump(invoices, file, indent=4, ensure_ascii=False)

    def generate_invoice(self):
        invoices_folder = os.path.join(os.getcwd(), "Invoices")
        if not os.path.exists(invoices_folder):
            os.makedirs(invoices_folder)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"invoice_{timestamp}.pdf"
        file_path = os.path.join(invoices_folder, file_name)
        invoice_data = self.to_dict()

        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Tiêu đề hóa đơn
        c.drawString(50, 750, "RECEIPT")
        c.drawString(50, 730, f"Date: {invoice_data['datetime']}")

        # Vẽ bảng danh sách sản phẩm
        y_position = 700
        c.drawString(50, y_position, "Product Name")
        c.drawString(150, y_position, "Quantity")
        c.drawString(250, y_position, "Price")


        y_position -= 20
        for item in invoice_data['cart']:
            c.drawString(50, y_position, item['name'])
            c.drawString(150, y_position, str(item['qty']))
            c.drawString(250, y_position, f"{item['unit_price']:,.0f}")
            y_position -= 20

        # Hiển thị tổng tiền
        y_position -= 30
        c.drawString(100, y_position, f"Total: {invoice_data['total']:,.0f}")

        y_position -= 40
        c.drawString(100, y_position, f"Tax: {invoice_data['tax']:,.0f}")

        y_position -= 50
        c.drawString(100, y_position, f"Total after tax: {invoice_data['total_after_tax']:,.0f}")

        c.save()
        print(f"Hóa đơn đã được lưu tại {file_name}")

