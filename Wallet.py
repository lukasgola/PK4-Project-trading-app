from Product import Product

class Wallet:
    def __init__(self):
        self.USD = 100000
        self.products = list()
        self.limit = list()

    def setWallet(self, u, p, l):
        self.USD = u
        self.products = p
        self.limits = l

    def getUSD(self):
        return self.USD
    
    def setUSD(self, value):
        self.USD = value
    
    def addProduct(self, type, buyPrice, buyDate, buyVolume, limit):
        self.products.append(Product(type, buyPrice, buyDate, buyVolume, limit))


    def getProducts(self):
        return self.products
    
    def addLimit(self, type, buyPrice, buyDate, buyVolume, limit):
        self.limit.append(Product(type, buyPrice, buyDate, buyVolume, limit))
    
    def getLimits(self):
        return self.limit

    #def getBalance(self):