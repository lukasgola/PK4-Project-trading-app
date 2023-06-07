class Product:
    def __init__(self, bP, bD, v):
        self.buyPrice = bP
        self.buyDate = bD
        self.volume = v

    def getBuyPrice(self):
        return self.buyPrice
    
    def getBuyDate(self):
        return self.buyDate
    
    def getVolume(self):
        return self.volume