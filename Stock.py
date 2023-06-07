from Product import Product

class Stock(Product):
    def __init__(self, bP, bD, v):
        super().__init__("stock", bP, bD, v)