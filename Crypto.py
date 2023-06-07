from Product import Product

class Crypto(Product):
    def __init__(self, bP, bD, v):
        super().__init__("crypto", bP, bD, v)
