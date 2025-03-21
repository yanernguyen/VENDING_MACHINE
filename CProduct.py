

import json
from typing import List, Dict


class Product:
    def __init__(self, name: str, category: str, price: float, stock: int):
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.name} (${self.price}) - {self.stock} in stock"

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
        }

