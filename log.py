import tkinter as tk
import hashlib
from tkinter import messagebox

from opertorPage import Opertor
from userPage import Userpage
from managerPage import Manager
from register import Register
import db.db_config as db
import db.Bike as Bike
import db.Order as Order
import db.Report as Report
import db.User as User
class Login:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 400
        window_height = 200
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(width=False, height=False)

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        self.login_label = tk.Label(self.login_frame, text="Login", font=("Helvetica", 16))
        self.login_label.grid(row=0, column=0, columnspan=2)

        self.login_username_label = tk.Label(self.login_frame, text="Email", font=("Helvetica", 12))
        self.login_username_label.grid(row=1, column=0)
        self.login_username = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.login_username.grid(row=1, column=1)

        self.login_password_label = tk.Label(self.login_frame, text="Password", font=("Helvetica", 12))
        self.login_password_label.grid(row=2, column=0)
        self.login_password = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12))
        self.login_password.grid(row=2, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, font=("Helvetica", 12))
        self.login_button.grid(row=3, column=0, pady=10)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_button.grid(row=3, column=1, pady=10)

        self.status_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.status_label.pack()

    def login(self):
        email = self.login_username.get()
        password = self.login_password.get()
        dict = db.query_data(User.login(email))
        if(len(dict)==0):
            messagebox.showerror("Error", "No user named {}".format(email))
            return
        checkmessage = dict[0]
        password_salt = checkmessage['salt'] + password
        hashed_password = hashlib.md5(password_salt.encode()).hexdigest()
        if(hashed_password==checkmessage['password']):

            if(checkmessage['user_type']=='User'):
                self.root.destroy()
                user_page = Userpage(checkmessage['id'])
                user_page.mainloop()

            elif(checkmessage['user_type']=='Operator'):
                self.root.destroy()
                opertor_view = Opertor(checkmessage['id'])
                opertor_view.mainloop()

            elif (checkmessage['user_type'] == 'Manager'):
                self.root.destroy()
                manager_page = Manager(checkmessage['id'])
                manager_page.mainloop()

            return
        else:
            messagebox.showerror("Error", "Wrong password")
            return

    def register(self):
        self.root.destroy()
        register_page = Register()
        register_page.run()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    login_page = Login()
    login_page.run()
