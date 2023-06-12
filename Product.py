class Product:
    def __init__(self, t, bP, bD, v):
        self.type = t
        self.buyPrice = bP
        self.buyDate = bD
        self.volume = v


    def getType(self):
        return self.type

    def getBuyPrice(self):
        return self.buyPrice
    
    def getBuyDate(self):
        return self.buyDate
    
    def getVolume(self):
        return self.volume