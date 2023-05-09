from Wallet import Wallet

class User:
    def __init__(self):
        self.username = "undefined"
        self.email = "undefined"
        self.password = "undefined"
        self.wallet = Wallet(0)
        

    def setUser(self, u, e, p):
        self.username = u
        self.email = e
        self.password = p

    def getUsername(self):
        return self.username
    
    def getEmail(self):
        return self.email
    
    def getPassword(self):
        return self.password