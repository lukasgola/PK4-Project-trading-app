from Crypto import Crypto

class Wallet:
    def __init__(self):
        self.USD = 100000
        self.fiat = []
        self.stocks = []
        self.crypto = list()

    def setWallet(self, u, f, s, c):
        self.USD = u
        self.fiat = f
        self.stocks = s
        self.crypto = c

    def getUSD(self):
        return self.USD
    
    def setUSD(self, value):
        self.USD = value
    
    def addProduct(self, type, buyPrice, buyDate, buyVolume):
        self.crypto.append(Crypto(type, buyPrice, buyDate, buyVolume))


    def getCryptos(self):
        return self.crypto

    #def getBalance(self):