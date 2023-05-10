import tkinter as tk
import customtkinter
from User import User

#Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

def setRedColor(x):
    x = "red"


loginBorderColor = "green"

def show_signIn(app):
    app.login = LoginFrame(app, fg_color="#161A1E")
    app.login.place(relx=0.5, rely=0.5,anchor=tk.CENTER)

def show_signUp(app):
    app.reg = RegisterFrame(app, fg_color="#161A1E")
    app.reg.place(relx=0.5, rely=0.5,anchor=tk.CENTER)

def show_trade(app):
    app.trade = TradeFrame(app, fg_color="#161A1E")
    app.trade.place(relx=0.5, rely=0.5,anchor=tk.CENTER)


class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        def signIn_event():
            
            email_text = self.email.get()
            password_text = self.password.get()

            if(email_text == "lukasz@gmail.com"):
                if(password_text == "roxi"):
                    self.destroy()
                    show_trade(app)
                else:
                    print("Wrong password")
            else:
                print("Wrong email")
                setRedColor(loginBorderColor)
            

        
        def goToSignUp_event():
            self.destroy()
            show_signUp(app)

        # add widgets onto the frame, for example:
        self.signInTitle = customtkinter.CTkLabel(self, text="Welcome!", font=("Roboto", 25))
        self.signInTitle.grid(row=0,column=0,padx=20,pady=20)

        self.email = customtkinter.CTkEntry(self, placeholder_text="Email",width=300,height=50,border_width=1, border_color=loginBorderColor, corner_radius=10, font=("Roboto", 14))
        self.email.grid(row=1,column=0,padx=20,pady=5)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Password",width=300,height=50,border_width=1,corner_radius=10, show="*", font=("Roboto", 14))
        self.password.grid(row=2, column=0,padx=20,pady=5)

        self.login = customtkinter.CTkButton(self, text="Sign In", font=("Roboto", 16), fg_color="#0DCB81", width=300, height=50, command=signIn_event)
        self.login.grid(row=3, column=0,padx=20,pady=5)


        self.dontHaveAccount = customtkinter.CTkLabel(self, text="Dont have account?", font=("Roboto", 12), fg_color="transparent", width=150, height=20)
        self.dontHaveAccount.grid(row=4, column=0,padx=20,pady=5, sticky=tk.W)

        self.goToSignUp = customtkinter.CTkButton(self, text="Sign Up", font=("Roboto", 12), fg_color="transparent", width=150, height=20, text_color="#0DCB81", hover="disable", command=goToSignUp_event)
        self.goToSignUp.grid(row=4, column=0,padx=20,pady=5, sticky=tk.E)

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        def signUp_event():
            self.destroy()
            show_trade(app)
        
        def goToSignIn_event():
            self.destroy()
            show_signIn(app)

        # add widgets onto the frame, for example:
        self.SignUpTitle = customtkinter.CTkLabel(self, text="Sign Up!", font=("Roboto", 25))
        self.SignUpTitle.grid(row=0,column=0,padx=20,pady=20)

        self.username = customtkinter.CTkEntry(self, placeholder_text="Username",width=300,height=50,border_width=1,corner_radius=10, font=("Roboto", 14))
        self.username.grid(row=1,column=0,padx=20,pady=5)

        self.email = customtkinter.CTkEntry(self, placeholder_text="Email",width=300,height=50,border_width=1,corner_radius=10, font=("Roboto", 14))
        self.email.grid(row=2,column=0,padx=20,pady=5)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Password",width=300,height=50,border_width=1,corner_radius=10, show="*", font=("Roboto", 14))
        self.password.grid(row=3, column=0,padx=20,pady=5)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Confirm Password",width=300,height=50,border_width=1,corner_radius=10, show="*", font=("Roboto", 14))
        self.password.grid(row=4, column=0,padx=20,pady=5)

        self.signUp = customtkinter.CTkButton(self, text="Sign Up", font=("Roboto", 16), fg_color="#0DCB81", width=300, height=50, command=signUp_event)
        self.signUp.grid(row=5, column=0,padx=20,pady=5)


        self.dontHaveAccount = customtkinter.CTkLabel(self, text="Have account?", font=("Roboto", 12), fg_color="transparent", width=150, height=20)
        self.dontHaveAccount.grid(row=6, column=0,padx=20,pady=5, sticky=tk.W)

        self.goToSignIn = customtkinter.CTkButton(self, text="Sign In", font=("Roboto", 12), fg_color="transparent", width=150, height=20, text_color="#0DCB81", hover="disable", command=goToSignIn_event)
        self.goToSignIn.grid(row=6, column=0,padx=20,pady=5, sticky=tk.E)


class TradeFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        self.chart = customtkinter.CTkFrame(self, width=900, height=600, fg_color="red")
        self.chart.grid(row=0, column=0)
        self.chart1 = customtkinter.CTkFrame(self, width=480, height=600, fg_color="green")
        self.chart1.grid(row=0, column=1)
        self.chart2 = customtkinter.CTkFrame(self, width=1280, height=320, fg_color="yellow")
        self.chart2.grid(row=1, column=0, columnspan=2)


        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Trading App")
        self.frame1 = customtkinter.CTkFrame(self, width=1280, height=720, fg_color="#161A1E")
        self.frame1.pack(fill=None, expand=False)

        show_signIn(self)
        


user = User()
app = App()
app.mainloop()
