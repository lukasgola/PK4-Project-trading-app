from tkinter import *
import customtkinter

import mplfinance as mpf

import yfinance as yf

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Interval required 1 minute
data = yf.download(tickers='BTC-USD', period='5d', interval='1h')

MAIN_COLOR = "#0DCB81"
SECOND_COLOR = '#F6475D'
BACK_COLOR = "#161A1E"

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

class TradeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        mc = mpf.make_marketcolors(up=MAIN_COLOR,down=SECOND_COLOR,
                            edge='inherit',
                            wick='black',
                            volume='in',
                            ohlc='i')
        s  = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)
        fig, axlist = mpf.plot(data, type="candle", volume=True, style=s)

        self.canvas = FigureCanvasTkAgg(fig)
        self.canvas.get_tk_widget().pack(self)
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Trading App")

        self.frame = TradeFrame(self)
        self.frame.pack()
        
        
    
root = App()
root.mainloop()
