class Wallet:
    def __init__(self):
        self.balance = 0
        self.fiat = []
        self.stocks = []
        self.crypto = []

    def setWallet(self, b, f, s, c):
        self.balance = b
        self.fiat = f
        self.stocks = s
        self.crypto = c