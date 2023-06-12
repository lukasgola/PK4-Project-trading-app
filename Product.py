class Product:
    def __init__(self, t, bP, bD, v, l):
        self.type = t
        self.buyPrice = bP
        self.buyDate = bD
        self.volume = v
        self.limit = l


    def getType(self):
        return self.type

    def getBuyPrice(self):
        return self.buyPrice
    
    def getBuyDate(self):
        return self.buyDate
    
    def getVolume(self):
        return self.volume
    
    def getLimit(self):
        return self.limit