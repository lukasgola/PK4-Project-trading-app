class Wallet:
    def __init__(self):
        self.USD = 100000
        self.fiat = []
        self.stocks = []
        self.crypto = []

    def setWallet(self, u, f, s, c):
        self.USD = u
        self.fiat = f
        self.stocks = s
        self.crypto = c

    def getUSD(self):
        return self.USD