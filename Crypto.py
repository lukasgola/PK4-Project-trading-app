from Product import Product

class Crypto(Product):
    def __init__(self,type, bP, bD, v, sl, tp):
        super().__init__(type, bP, bD, v, sl, tp)
