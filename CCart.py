
import json
from typing import List, Dict
from CProduct import *
class Cart:
    def __init__(self):
        self.items: Dict[str, int] = {}  #giúp lưu trữ giỏ hàng theo tên sản phẩm và số lượng.

    def add_item(self, product: Product, quantity: int):
        if product.name in self.items:
            self.items[product.name] += quantity
        else:
            self.items[product.name] = quantity
        product.stock -= quantity

    def remove_item(self, product: Product):
        if product.name in self.items:
            quantity = self.items.pop(product.name)
            product.stock += quantity

    def clear(self):
        self.items.clear()

    def get_total(self, products: List[Product]) -> float:
        total = 0.0
        for product_name, quantity in self.items.items():
            for product in products:
                if product.name == product_name:
                    total += product.price * quantity
                    break
        return total

    def to_dict(self):
        return self.items

    def __str__(self):
        return "\n".join([f"{name} x {quantity}" for name, quantity in self.items.items()])