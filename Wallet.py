from Crypto import Crypto

class Wallet:
    def __init__(self):
        self.USD = 100000
        self.fiat = []
        self.stocks = []
        self.crypto = list()
        self.limit = list()

    def setWallet(self, u, f, s, c):
        self.USD = u
        self.fiat = f
        self.stocks = s
        self.crypto = c

    def getUSD(self):
        return self.USD
    
    def setUSD(self, value):
        self.USD = value
    
    def addProduct(self, type, buyPrice, buyDate, buyVolume, stopLoss, takeProfit):
        self.crypto.append(Crypto(type, buyPrice, buyDate, buyVolume, stopLoss, takeProfit))


    def getCryptos(self):
        return self.crypto
    
    def addLimit(self, type, buyPrice, buyDate, buyVolume, stopLoss, takeProfit):
        self.limit.append(Crypto(type, buyPrice, buyDate, buyVolume, stopLoss, takeProfit))
    
    def getLimit(self):
        return self.limit

    #def getBalance(self):