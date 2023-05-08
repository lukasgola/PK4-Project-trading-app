import tkinter as tk
import customtkinter

#Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.LoginTitle = customtkinter.CTkLabel(self, text="Zaloguj się!", font=("Roboto", 25))
        self.LoginTitle.grid(row=0,column=0,padx=20,pady=20)

        self.email = customtkinter.CTkEntry(self, placeholder_text="Email",width=300,height=50,border_width=1,corner_radius=10)
        self.email.grid(row=1,column=0,padx=20,pady=5)

        self.password = customtkinter.CTkEntry(self, placeholder_text="Password",width=300,height=50,border_width=1,corner_radius=10)
        self.password.grid(row=2, column=0,padx=20,pady=5)

        self.zaloguj = customtkinter.CTkButton(self, text="ZALOGUJ", font=("Roboto", 16), fg_color="#0DCB81", width=300, height=50)
        self.zaloguj.grid(row=3, column=0,padx=20,pady=5)

        self.forgotPassword = customtkinter.CTkButton(self, text="Zapomniałeś hasła?", font=("Roboto", 12), fg_color="transparent", width=300, height=20, hover="disable")
        self.forgotPassword.grid(row=4, column=0,padx=20,pady=5)

        self.forgotPassword = customtkinter.CTkButton(self, text="Zarejestruj się?", font=("Roboto", 12), fg_color="transparent", width=300, height=20, text_color="#0DCB81", hover="disable")
        self.forgotPassword.grid(row=5, column=0,padx=20,pady=0)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("Trading App")
        frame1 = tk.Frame(self, width=1280, height=720, background="#161A1E")
        frame1.pack(fill=None, expand=False)

        # add widgets to app
        self.my_frame = MyFrame(self, fg_color="#161A1E")
        self.my_frame.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
        
    # add methods to app
    def button_click(self):
        print("button click")


app = App()
app.mainloop()