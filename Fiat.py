from Product import Product

class Fiat(Product):
    def __init__(self, bP, bD, v):
        super().__init__("fiat", bP, bD, v)