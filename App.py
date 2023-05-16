import tkinter as tk
import customtkinter
import re
import sqlite3
import hashlib

#Charts
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import mplfinance as mpf

import yfinance as yf

import matplotlib.animation as animation


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
        super().__init__(master, width=800, height=520, **kwargs)

        data = yf.download(tickers='BTC-USD', period='2d', interval='5m')

        mc = mpf.make_marketcolors(up=MAIN_COLOR,down=SECOND_COLOR,
                            edge='inherit',
                            wick='black',
                            volume='in',
                            ohlc='i')
        s  = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

        pkwargs=dict(type='candle', mav=(10,20))

        fig, axes = mpf.plot(data.iloc[len(data)-50:len(data)],figsize=(4,3), returnfig=True, volume=True, style=s, **pkwargs )

        def animate(ival):    
            idf2 = yf.download(tickers='BTC-USD', period='2d', interval='5m')

            data2 = idf2.iloc[len(idf2)-50:len(idf2)]
            axes[0].clear()
            fig, axes = mpf.plot(data2, returnfig=True, volume=True, style=s, **pkwargs )

        #ani = animation.FuncAnimation(fig, animate, interval=1000)
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class TradeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.chart = ChartFrame(self, fg_color="red")
        self.chart.grid(row=0, column=0)
        self.chart1 = customtkinter.CTkFrame(self, width=480, height=520, fg_color="green")
        self.chart1.grid(row=0, column=1)

        def _quit():
            app.quit()     # stops mainloop
            app.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate


        self.button = customtkinter.CTkButton(self, width=1280, height=200, text="Quit", command=_quit)
        self.button.grid(row=1, column=0, columnspan=2)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Trading App")

        
        self.container = customtkinter.CTkFrame(self, fg_color = BACK_COLOR)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        
        register = RegisterFrame(self.container, fg_color=BACK_COLOR)

        self.frames[RegisterFrame] = register

        register.place(relx=0.5, rely=0.5,anchor=tk.CENTER)

        self.show_frame(TradeFrame, RegisterFrame)
        
    def show_frame(self, cont, old): 
        oldFrame = self.frames[old]
        oldFrame.destroy()
        frame = cont(self.container, fg_color = BACK_COLOR)
        self.frames[cont] = frame
        frame.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
        

user = User()
app = App()
app.mainloop()
