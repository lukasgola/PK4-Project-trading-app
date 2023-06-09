import tkinter as tk
import customtkinter
import re
import sqlite3
import hashlib
import time

from datetime import datetime

#Charts
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


import mplfinance as mpf
import yfinance as yf


#Classes
from User import User

#Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

MAIN_COLOR = "#0DCB81"
SECOND_COLOR = '#F6475D'
BACK_COLOR = "#161A1E"

#Database
def check_data(email, password):
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()

    password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT * FROM userdata WHERE email = ? AND password = ?",(email, password))

    if cursor.fetchall():
        connection.close()
        return True
    else:
        connection.close()
        return False

def check_username(username):
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM userdata WHERE username = ?",(username,))

    if cursor.fetchall():
        connection.close()
        return True
    else:
        connection.close()
        return False

def check_email(email):
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM userdata WHERE email = ?",(email,))

    if cursor.fetchall():
        connection.close()
        return True
    else:
        connection.close()
        return False
    
def check_password(password):
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()

    password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT * FROM userdata WHERE password = ?",(password,))

    if cursor.fetchall():
        connection.close()
        return True
    else:
        connection.close()
        return False

def get_username(email):
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()

    cursor.execute("SELECT username FROM userdata WHERE email = ?",(email,))

    usr = cursor.fetchall()

    if usr:
        connection.close()
        return usr[0]
    else:
        connection.close()
        return "None"

def save_data(username, email, password):
    connection = sqlite3.connect("userdata.db")
    cursor = connection.cursor()

    password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("""CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )""")

    cursor.execute("INSERT INTO userdata (username, email, password) VALUES (?, ?, ?)",(username, email, password))

    connection.commit()


exchange = "BTC-USD"
period = '2d'
interval = '2m'
interval_ms = 2000
DatCounter = 9000

current_price = 0

chartLoad = True
DataPace = "tick"


ival = 0
data = yf.download(tickers=exchange, period=period, interval=interval)

refresher_data = yf.download(tickers=exchange, period=period, interval='1m')

print(data)

def changeExchange(ex):
    global exchange
    global DatCounter
    global data
    global refresher_data

    exchange = ex
    DatCounter = 9000
    data = yf.download(tickers=exchange, period=period, interval=interval)
    refresher_data = yf.download(tickers=exchange, period=period, interval='1m')

def changePeriod(pe):
    global period
    global data

    period = pe
   
    data = yf.download(tickers=exchange, period=period, interval=interval)

def changeInterval(int, ms):
    global interval
    global interval_ms
    global data
    global ival


    interval_ms = ms*1000
    interval = int
    ival = 0

    data = yf.download(tickers=exchange, period=period, interval=interval)



class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # add widgets onto the frame, for example:
        self.signInTitle = customtkinter.CTkLabel(self, text="Welcome!", font=("Roboto", 25))
        self.signInTitle.grid(row=0,column=0,padx=20,pady=20)

        self.email = customtkinter.CTkEntry(self, placeholder_text="Email", width=300,height=50,border_width=1, corner_radius=10, font=("Roboto", 14),)
        self.email.grid(row=1,column=0,padx=20,pady=5)

        self.emailError = customtkinter.CTkLabel(self, text="", font=("Roboto", 10), height=10)
        self.emailError.grid(row=2,column=0,padx=25,pady=0, sticky=tk.W)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Password",width=300,height=50,border_width=1,corner_radius=10, show="*", font=("Roboto", 14))
        self.password.grid(row=3, column=0,padx=20,pady=5)

        self.passwordError = customtkinter.CTkLabel(self, text="", font=("Roboto", 10), height=10)
        self.passwordError.grid(row=4,column=0,padx=25,pady=0, sticky=tk.W)

        self.signIn = customtkinter.CTkButton(self, text="Sign In", font=("Roboto", 16), fg_color=MAIN_COLOR, width=300, height=50, command=self.signIn_event)
        self.signIn.grid(row=5, column=0,padx=20,pady=5)


        self.dontHaveAccount = customtkinter.CTkLabel(self, text="Dont have account?", font=("Roboto", 12), fg_color="transparent", width=150, height=20)
        self.dontHaveAccount.grid(row=6, column=0,padx=20,pady=5, sticky=tk.W)

        self.goToSignUp = customtkinter.CTkButton(self, text="Sign Up", font=("Roboto", 12), fg_color="transparent", width=150, height=20, text_color=MAIN_COLOR, hover="disable", command=self.goToSignUp_event)
        self.goToSignUp.grid(row=6, column=0,padx=20,pady=5, sticky=tk.E)
    

    def signIn_event(self):
        emailText = self.email.get()
        passwordText = self.password.get()
        

        if check_data(emailText, passwordText):
            user.setUser(get_username(emailText), emailText, passwordText)
            print(user.getUsername())
            app.show_frame(TradeFrame, LoginFrame)
        if not check_email(emailText):
            self.show_message(self.emailError, "Email not found")
            return False
        elif check_email(emailText) and not check_data(emailText, passwordText):
            self.show_message(self.passwordError, "Wrong password")
            return False
            
        
    def goToSignUp_event(self):
        app.show_frame(RegisterFrame, LoginFrame)
    
    def show_message(self, atributte, error='', color='black'):
        atributte.configure(text=error)
        atributte.configure(text_color="red")

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        email_vcmd = (self.register(self.validate_email), '%P')
        password_vcmd = (self.register(self.validate_password), '%P')

        # add widgets onto the frame, for example:
        self.SignUpTitle = customtkinter.CTkLabel(self, text="Sign Up!", font=("Roboto", 25))
        self.SignUpTitle.grid(row=0,column=0,padx=20,pady=20)

        self.username = customtkinter.CTkEntry(self, placeholder_text="Username",width=300,height=50,border_width=1,corner_radius=10, font=("Roboto", 14))
        self.username.configure(validate='focusout', validatecommand=self.validate_username)
        self.username.grid(row=1,column=0,padx=20,pady=5)

        self.usernameError = customtkinter.CTkLabel(self, text="", font=("Roboto", 10), height=10)
        self.usernameError.grid(row=2,column=0,padx=25,pady=0, sticky=tk.W)

        self.email = customtkinter.CTkEntry(self, placeholder_text="Email",width=300,height=50,border_width=1,corner_radius=10, font=("Roboto", 14))
        self.email.configure(validate='focusout', validatecommand=email_vcmd)
        self.email.grid(row=3,column=0,padx=20,pady=5)
        

        self.emailError = customtkinter.CTkLabel(self, text="", font=("Roboto", 10), height=10)
        self.emailError.grid(row=4,column=0,padx=25,pady=0, sticky=tk.W)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Password",width=300,height=50,border_width=1,corner_radius=10, show="*", font=("Roboto", 14))
        self.password.configure(validate='focusout', validatecommand=password_vcmd)
        self.password.grid(row=5, column=0,padx=20,pady=5)

        self.passwordError = customtkinter.CTkLabel(self, text="", font=("Roboto", 10), height=10)
        self.passwordError.grid(row=6,column=0,padx=25,pady=0, sticky=tk.W)

        self.passwordRepeat = customtkinter.CTkEntry(self, placeholder_text="Confirm Password",width=300,height=50,border_width=1,corner_radius=10, show="*", font=("Roboto", 14))
        self.passwordRepeat.configure(validate='focusout', validatecommand=self.validate_password_match)
        self.passwordRepeat.grid(row=7, column=0,padx=20,pady=5)

        self.passwordMatchError = customtkinter.CTkLabel(self, text="", font=("Roboto", 10), height=10)
        
        self.passwordMatchError.grid(row=8,column=0,padx=25,pady=0, sticky=tk.W)

        self.signUp = customtkinter.CTkButton(self, text="Sign Up", font=("Roboto", 16), fg_color=MAIN_COLOR, width=300, height=50, command=self.signUp_event)
        self.signUp.grid(row=9, column=0,padx=20,pady=5)


        self.dontHaveAccount = customtkinter.CTkLabel(self, text="Have account?", font=("Roboto", 12), fg_color="transparent", width=150, height=20)
        self.dontHaveAccount.grid(row=10, column=0,padx=20,pady=5, sticky=tk.W)

        self.goToSignIn = customtkinter.CTkButton(self, text="Sign In", font=("Roboto", 12), fg_color="transparent", width=150, height=20, text_color=MAIN_COLOR, hover="disable", command=self.goToSignIn_event)
        self.goToSignIn.grid(row=10, column=0,padx=20,pady=5, sticky=tk.E)

    def signUp_event(self):
            username = self.username.get()
            email = self.email.get()
            password = self.password.get()

            if not check_username(username) and not check_email(email) and self.validate_email(email) and self.validate_password(password):
                save_data(username, email, password)
                app.show_frame(TradeFrame, RegisterFrame)
        
    def goToSignIn_event(self):
        app.show_frame(LoginFrame, RegisterFrame)

    def show_message(self, atributte, error='', color='black'):
        atributte.configure(text=error)
        atributte.configure(text_color="red")

    def validate_username(self):
        if check_username(self.username.get()):
            self.show_message(self.usernameError, "Username in use")
            return False
            
        self.show_message(self.usernameError, "")
        return True
        

    def validate_email(self, value):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if value:
            if check_email(value):
                self.show_message(self.emailError, "Email in use")
                return False
            if re.fullmatch(pattern, value) is None:
                self.show_message(self.emailError, "Invalid email")
                return False
            
        self.show_message(self.emailError, "")
        return True
    
    def validate_password(self, value):
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        if value:
            if re.fullmatch(pattern, value) is None:
                self.show_message(self.passwordError, "Invalid password")
                return False

        self.show_message(self.passwordError, "")
        return True
    
    def validate_password_match(self):
        if re.fullmatch(self.password.get(), self.passwordRepeat.get()) is None:
            self.show_message(self.passwordMatchError, "Passwords not match")
            return False
        
        self.show_message(self.passwordMatchError)
        return True

class ChartFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        global data
        global period
        global interval
        global interval_ms

        #data = yf.download(tickers=exchange, period=period, interval=interval)

        mc = mpf.make_marketcolors(up=MAIN_COLOR, down=SECOND_COLOR, edge={'up': MAIN_COLOR, 'down': SECOND_COLOR}, volume=MAIN_COLOR)
        s = mpf.make_mpf_style(marketcolors=mc, base_mpf_style="nightclouds")
        pkwargs=dict(type='candle', mav=(10,20), style=s)
        
        if interval_ms == 1000:
            fig, axes = mpf.plot(data.iloc[690:740], figsize=(8,5), returnfig=True,volume=True,**pkwargs)
        if interval_ms == 2000:
            fig, axes = mpf.plot(data.iloc[325:375], figsize=(4,3),panel_ratios=(3,1), returnfig=True,volume=True,**pkwargs)
        if interval_ms == 5000:
            fig, axes = mpf.plot(data.iloc[100:150], figsize=(8,5), returnfig=True,volume=True,**pkwargs)
        if interval_ms == 15000:
            fig, axes = mpf.plot(data.iloc[0:51], figsize=(8,5), returnfig=True,volume=True,**pkwargs)


            
        ax1 = axes[0]
        ax2 = axes[2]

        def animate(ival):

            global refreshRate
            global DatCounter
        

            if chartLoad:
                if DataPace == "tick":
                    try:
                        if (50+ival) > len(data):
                            print('no more data to plot')
                            ani.event_source.interval *= 3
                            if ani.event_source.interval > 12000:
                                exit()
                            return
                        
                        
                        if interval_ms == 1000:
                            idf = data.iloc[690+ival:740+ival]
                            print(data.iloc[739+ival:740+ival])
                        if interval_ms == 2000:
                            idf = data.iloc[327+ival:377+ival]
                            print(data.iloc[376+ival:377+ival])
                        if interval_ms == 5000:
                            idf = data.iloc[102+ival:152+ival]
                            print(data.iloc[151+ival:152+ival])
                        if interval_ms == 15000:
                            idf = data.iloc[1+ival:51+ival]
                            print(data.iloc[50+ival:51+ival])


                        ax1.clear()
                        ax2.clear()
                        mpf.plot(idf, ax=ax1, volume=ax2, **pkwargs)
                        ax1.set_title(exchange)
                    
                    except Exception as e:
                        print("Failed because of", e)


        #ani = animation.FuncAnimation(fig, animate, interval=interval_ms)


        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class BuyLimitFrame(customtkinter.CTkFrame):
    def __init__(self, master, trade, **kwargs):
        super().__init__(master, **kwargs)
        
        # add widgets onto the frame, for example:

        self.actprice  = tk.DoubleVar(master=self, value=0)
        self.toPay  = tk.DoubleVar(master=self, value=0)
        self.ratioValue = tk.DoubleVar(master=self, value=0)
        self.volumeValue = tk.DoubleVar(master=self, value=0)

        self.trade = trade

        self.left = customtkinter.CTkFrame(self, width=70, fg_color=BACK_COLOR)
        self.left.grid(row=0, column=0, rowspan=8)

        self.left = customtkinter.CTkFrame(self, width=70, fg_color=BACK_COLOR)
        self.left.grid(row=0, column=3, rowspan=8)

        self.buy = customtkinter.CTkButton(self, text="BUY", font=("Roboto", 16, "bold"), fg_color=MAIN_COLOR, hover=False, width=130, height=30, command=self.buyClick)
        self.buy.grid(row=1, column=1,padx=10,pady=5)

        self.sell = customtkinter.CTkButton(self, text="SELL", font=("Roboto", 16, "bold"), fg_color="#39434D", hover=False, width=130, height=30, command=self.sellClick)
        self.sell.grid(row=1, column=2,padx=10,pady=5)
    
        self.price = customtkinter.CTkEntry(self, textvariable=self.actprice, placeholder_text="Limit", state="disabled", width=300, height=50, border_width=1, corner_radius=10, font=("Roboto", 14))
        self.price.grid(row=2,column=1, padx=20,pady=5, columnspan=2)

        self.volume = customtkinter.CTkSlider(self, from_=0, to=100, variable=self.ratioValue, command=self.slider_event)
        self.volume.grid(row=3,column=1, padx=20,pady=5, columnspan=2)

        self.volumeShow = customtkinter.CTkLabel(self, textvariable=self.ratioValue, text=user.getEmail(), font=("Roboto", 16, "bold"))
        self.volumeShow.grid(row=4, column=1,padx=0, pady=5, sticky=tk.E)

        self.volumeShow2 = customtkinter.CTkLabel(self, text="%", font=("Roboto", 16, "bold"))
        self.volumeShow2.grid(row=4, column=2,padx=0, pady=5, sticky=tk.W)

        self.stopLoss = customtkinter.CTkCheckBox(self, text="Stop Loss", font=("Roboto", 14))
        self.stopLoss.grid(row=5, column=1, padx=20, sticky=tk.W)

        self.stopLossValue = customtkinter.CTkEntry(self, placeholder_text="Stop Loss", width=300, height=50, border_width=1, corner_radius=10, font=("Roboto", 14))
        self.stopLossValue.grid(row=6,column=1, padx=20,pady=5, columnspan=2)

        self.takeProfit = customtkinter.CTkCheckBox(self, text="Take Profit", font=("Roboto", 14))
        self.takeProfit.grid(row=7, column=1, padx=20, sticky=tk.W)

        self.takeProfitValue = customtkinter.CTkEntry(self, placeholder_text="Take Profit", width=300, height=50, border_width=1, corner_radius=10, font=("Roboto", 14))
        self.takeProfitValue.grid(row=8,column=1, padx=20,pady=5, columnspan=2)

        self.needToPay = customtkinter.CTkEntry(self, textvariable=self.toPay, placeholder_text="Limit", state="disabled", width=300, height=50, border_width=1, corner_radius=10, font=("Roboto", 14))
        self.needToPay.grid(row=9,column=1, padx=20,pady=5, columnspan=2)

        self.stocks = customtkinter.CTkLabel(self, textvariable=self.volumeValue, font=("Roboto", 12, "bold"))
        self.stocks.grid(row=10, column=1,padx=20,pady=5, columnspan=2)
        
        self.confirm = customtkinter.CTkButton(self, text="BUY", font=("Roboto", 16, "bold"), fg_color=MAIN_COLOR, hover=True, width=300, height=50, command=self.confirm)
        self.confirm.grid(row=11, column=1, columnspan=2, padx=10,pady=10)

        self.Refresher()

    
    def Refresher(self):
        global text
        global ival
        global refresher_data
        global interval_ms
        global current_price

        ival+=1
        output = refresher_data[737+ival:738+ival]['Open']
        output = output.to_list()
        current_price = round(output[0],2)

        self.actprice.set(value=current_price)
        ratio = round(user.wallet.getUSD()*(self.ratioValue.get()/100),5)
        self.volumeValue.set(value=round(ratio/current_price,5))
        self.toPay.set(value=ratio)

        self.after(1000, self.Refresher) # every second...

    def slider_event(self, value):
        self.ratioValue.set(value=round(value, 2))

    def confirm(self):
        self.trade.add_transaction(self.toPay.get(),self.volumeValue.get())
        self.ratioValue.set(value=0)

    def buyClick(self):
        user.wallet.getCryptos()
        self.sell.configure(fg_color="#39434D")
        self.buy.configure(fg_color=MAIN_COLOR)
        self.confirm.configure(text="SELL", fg_color=MAIN_COLOR)

    def sellClick(self):
        self.buy.configure(fg_color="#39434D")
        self.sell.configure(fg_color=SECOND_COLOR)
        self.confirm.configure(text="SELL", fg_color=SECOND_COLOR)

    
    

    def show_message(self, atributte, error='', color='black'):
        atributte.configure(text=error)
        atributte.configure(text_color="red")

class TradesInfo(customtkinter.CTkFrame):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, width, height, **kwargs)
        
        self.tradePrice = 0
        self.volumeVal = 0
        self.width = width

        self.usd = user.wallet.getUSD()
        cryptoList = user.wallet.getCryptos()
        for t in cryptoList:
            print(type(t))

        


        # add widgets onto the frame, for example:
        self.container = customtkinter.CTkFrame(self, width=800, height=height, fg_color = BACK_COLOR)
        self.container.grid(row=0, column=0, padx=0, sticky=tk.NW)

        self.right = customtkinter.CTkFrame(self, width=480, height=height+40, fg_color = BACK_COLOR)
        self.right.grid(row=0, column=1, rowspan=2, padx=0, sticky=tk.NE)
        
        
        self.new = customtkinter.CTkFrame(self.container, width=800, height=100, fg_color = "#39434D")
        self.new.grid(row=0, column=0, padx=0)
        
        self.dateStr = customtkinter.CTkLabel(self.new, text="Datetime", width=200)
        self.dateStr.grid(row=0, column=0, padx=0)
        
        self.cur_priceStr = customtkinter.CTkLabel(self.new, text="Current Price", width=150)
        self.cur_priceStr.grid(row=0, column=2, padx=0)

        self.priceStr = customtkinter.CTkLabel(self.new, text="Buy Price", width=150)
        self.priceStr.grid(row=0, column=3, padx=0)

        self.volumeStr = customtkinter.CTkLabel(self.new, text="Volume", width=150)
        self.volumeStr.grid(row=0, column=4, padx=0)

        self.priceDiffStr = customtkinter.CTkLabel(self.new, text="Price Diff", width=150)
        self.priceDiffStr.grid(row=0, column=5, padx=0)

        self.container1 = customtkinter.CTkScrollableFrame(self.container, width=800, height=200, fg_color = BACK_COLOR )
        self.container1.grid(row=1, column=0, sticky=tk.SW)




        self.username = customtkinter.CTkLabel(self.right, text=user.getUsername(), font=("Roboto", 16, "bold"), width=480)
        self.username.grid(row=0, column=0, columnspan=2, padx=0,pady=5)

        self.email = customtkinter.CTkLabel(self.right, text=user.getEmail(), font=("Roboto", 16, "bold"), width=480)
        self.email.grid(row=1, column=0, columnspan=2, padx=0,pady=5)

        self.usd = customtkinter.CTkLabel(self.right, text="USD", font=("Roboto", 16, "bold"), width=180)
        self.usd.grid(row=2, column=0,padx=10,pady=5)

        self.fiat = customtkinter.CTkLabel(self.right, text="Fiat", font=("Roboto", 16, "bold"), width=180)
        self.fiat.grid(row=3, column=0,padx=10,pady=5)

        self.crypto = customtkinter.CTkLabel(self.right, text="Stocks", font=("Roboto", 16, "bold"), width=180)
        self.crypto.grid(row=4, column=0,padx=10,pady=5)

        self.stocks = customtkinter.CTkLabel(self.right, text="Crypto", font=("Roboto", 16, "bold"), width=180)
        self.stocks.grid(row=5, column=0,padx=10,pady=5)

        self.usdValue = customtkinter.CTkLabel(self.right, text=user.wallet.getUSD(), font=("Roboto", 16, "bold"), width=260)
        self.usdValue.grid(row=2, column=1,padx=10,pady=5)

        self.fiatValue = customtkinter.CTkLabel(self.right, text="0.00", font=("Roboto", 16, "bold"), width=260)
        self.fiatValue.grid(row=3, column=1,padx=10,pady=5)

        self.cryptoValue = customtkinter.CTkLabel(self.right, text="0.00", font=("Roboto", 16, "bold"), width=260)
        self.cryptoValue.grid(row=4, column=1,padx=10,pady=5)

        self.stocksValue = customtkinter.CTkLabel(self.right, text="0.00", font=("Roboto", 16, "bold"), width=260)
        self.stocksValue.grid(row=5, column=1,padx=10,pady=5)
        
        self.verses = {}

        self.Refresher()


    def Refresher(self):
        global text
        global ival
        global refresher_data
        global interval_ms
        global current_price

        output = refresher_data[738+ival:739+ival]['Open']
        output = output.to_list()
        if self.verses:
            if self.volumeVal != 0:
                for t in self.verses:
                    diff = round((output[0] - (self.tradePrice/self.volumeVal))*self.volumeVal,2)
                    color = "white"
                    if diff > 0:
                        color = MAIN_COLOR
                    else:
                        color= SECOND_COLOR
                    self.priceDiff.configure(text=diff, text_color=color)

        self.after(1000, self.Refresher) # every second...


    def add_transaction(self,  price, volume):

        global current_price

        if volume != 0:
            self.tradePrice = price
            self.volumeVal = volume

            new = customtkinter.CTkFrame(self.container1, width=self.width, fg_color = "#39434D")
            self.verses[customtkinter.CTkFrame] = new
            new.pack(side = tk.TOP, pady = 5, padx = 0)
            self.date = customtkinter.CTkLabel(new, text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), width=200)
            self.date.grid(row=0, column=0, padx=0)

            self.cur_price = customtkinter.CTkLabel(new, text=current_price, width=150)
            self.cur_price.grid(row=0, column=2, padx=0)

            self.price = customtkinter.CTkLabel(new, text=price, width=150)
            self.price.grid(row=0, column=3, padx=0)

            self.volume = customtkinter.CTkLabel(new, text=volume, width=150)
            self.volume.grid(row=0, column=4, padx=0)

            self.priceDiff = customtkinter.CTkLabel(new, text="0.00", width=150)
            self.priceDiff.grid(row=0, column=5, padx=0)

            self.usdValue.configure(text=round(user.wallet.getUSD()-price,2))

            user.wallet.setUSD(user.wallet.getUSD()-price)
            user.wallet.addProduct(exchange, price, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), volume)


    def update(self):
        self.text.configure(text="New Hello")

    def show_message(self, atributte, error='', color='black'):
        atributte.configure(text=error)
        atributte.configure(text_color="red")


class TradeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        self.charts = {}
        chart = customtkinter.CTkFrame(self, width=800, height=520, fg_color="grey")
        #chart = ChartFrame(self)
        self.charts[ChartFrame] = chart
        chart.grid(row=0, column=0, sticky=tk.W)

        
        
        self.trades = {}
        trade = TradesInfo(self, width=1280, height=200, fg_color=BACK_COLOR)
        self.trades[TradesInfo] = trade
        trade.grid(row=1, column=0, columnspan=2)


        self.frames = {}
        buy = BuyLimitFrame(self, trade, width=480, height=520, fg_color=BACK_COLOR)
        self.frames[BuyLimitFrame] = buy
        buy.grid(row=0, column=1)


    def show_chart(self, cont, old): 
        print("Printing")
        oldChart = self.charts[old]
        oldChart.destroy()
        chart = cont(self)
        self.charts[cont] = chart
        chart.grid(row=0, column=0, sticky=tk.W)

    def show_trades(self, cont, old): 
        print("Printing")
        oldTrade = self.trades[old]
        oldTrade.destroy()
        trade = cont(self, width=1280, height=200, fg_color = BACK_COLOR)
        self.trades[cont] = trade
        trade.grid(row=1, column=0, columnspan=2)




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x780")
        self.title("Trading App")
        
        self.container = customtkinter.CTkFrame(self, fg_color = BACK_COLOR)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)


        exchangeChoice = tk.Menu(menubar, tearoff=0)
        exchangeChoice.add_command(label="BTC-USD", command=lambda: changeExchange("BTC-USD"))
        exchangeChoice.add_command(label="ETH-USD", command=lambda: changeExchange("ETH-USD"))

        periodChoice = tk.Menu(menubar, tearoff=0)
        periodChoice.add_command(label="2d", command=lambda: changePeriod("2d"))


        intervalChoice = tk.Menu(menubar, tearoff=0)
        intervalChoice.add_command(label="1m", command=lambda: [changeInterval("1m", 1), trade.show_chart(ChartFrame, ChartFrame)] )
        intervalChoice.add_command(label="2m", command=lambda: [changeInterval("2m", 2), trade.show_chart(ChartFrame, ChartFrame)])
        intervalChoice.add_command(label="5m", command=lambda: [changeInterval("5m", 5), trade.show_chart(ChartFrame, ChartFrame)])
        intervalChoice.add_command(label="15m", command=lambda: [changeInterval("15m", 15), trade.show_chart(ChartFrame, ChartFrame)])

        menubar.add_cascade(label="Exchange", menu=exchangeChoice)
        menubar.add_cascade(label="Period", menu=periodChoice)
        menubar.add_cascade(label="Interval", menu=intervalChoice)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}
        trade = TradeFrame(self.container, fg_color=BACK_COLOR)
        self.frames[TradeFrame] = trade
        trade.place(relx=0.5, rely=0.5,anchor=tk.CENTER)


        self.show_frame(TradeFrame, TradeFrame)
        
    def show_frame(self, cont, old): 
        oldFrame = self.frames[old]
        oldFrame.destroy()
        frame = cont(self.container, fg_color = BACK_COLOR)
        self.frames[cont] = frame
        frame.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
        

user = User()
app = App()
app.mainloop()
