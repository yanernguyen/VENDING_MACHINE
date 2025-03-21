import json
from CProduct import *
from CCart import *


class SmartMartFunctions:
    def __init__(self):
        self.products = self.load_products()
        self.cart = Cart()
        self.load_cart()

    def load_products(self) -> List[Product]:
        try:
            with open("data/products.json", "r") as file:
                products_data = json.load(file)
                return [Product(**data) for data in products_data]
        except FileNotFoundError:
            return []

    def save_products(self):
        with open("data/products.json", "w") as file:
            json.dump([product.to_dict() for product in self.products], file, indent=4)

    def load_cart(self):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
                self.cart.items = cart_data
        except FileNotFoundError:
            self.cart.items = {}

    def save_cart(self):
        with open("data/cart.json", "w") as file:
            json.dump(self.cart.to_dict(), file, indent=4)

    def search_products(self, keyword: str) -> List[Product]:
        return [product for product in self.products if keyword.lower() in product.name.lower()]

    def add_to_cart(self, product_name: str) -> bool:
        for product in self.products:
            if product.name == product_name:
                if product.stock > 0:
                    self.cart.add_item(product, 1)
                    return True
                else:
                    return False
        return False

    def remove_from_cart(self, product_name: str) -> bool:
        for product in self.products:
            if product.name == product_name:
                self.cart.remove_item(product)
                return True
        return False

    def checkout(self) -> float:
        total = self.cart.get_total(self.products)
        self.cart.clear()
        return total