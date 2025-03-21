import json
from typing import Optional


class Product:
    _next_id = 1

    def __init__(self, name: str, category: str, price: float,
                 stock: int, image: str = None, id: str = None):

        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.image = image
        self.id = id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "image": self.image,
        }

    def is_valid(self) -> bool:
        return (
                isinstance(self.name, str) and self.name.strip() != "" and
                isinstance(self.category, str) and self.category.strip() != "" and
                self.price > 0 and
                self.stock >= 0
        )

