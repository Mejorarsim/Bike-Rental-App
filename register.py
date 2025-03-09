import tkinter as tk
import hashlib
import random
import string
from tkinter import messagebox
import db.db_config as db
import db.Bike as Bike
import db.Order as Order
import db.Report as Report
import db.User as User
class Register:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registration Page")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 400
        window_height = 250

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.resizable(width=False, height=False)

        self.reg_frame = tk.Frame(self.root)
        self.reg_frame.pack(pady=20)

        self.reg_label = tk.Label(self.reg_frame, text="Registration", font=("Helvetica", 16))
        self.reg_label.grid(row=0, column=0, columnspan=2)

        self.reg_username_label = tk.Label(self.reg_frame, text="Username", font=("Helvetica", 12))
        self.reg_username_label.grid(row=1, column=0)
        self.reg_username = tk.Entry(self.reg_frame, font=("Helvetica", 12))
        self.reg_username.grid(row=1, column=1)

        self.reg_email_label = tk.Label(self.reg_frame, text="Email", font=("Helvetica", 12))
        self.reg_email_label.grid(row=2, column=0)
        self.reg_email = tk.Entry(self.reg_frame, font=("Helvetica", 12))
        self.reg_email.grid(row=2, column=1)

        self.reg_phone_label = tk.Label(self.reg_frame, text="Phone", font=("Helvetica", 12))
        self.reg_phone_label.grid(row=3, column=0)
        self.reg_phone = tk.Entry(self.reg_frame, font=("Helvetica", 12))
        self.reg_phone.grid(row=3, column=1)

        self.reg_password_label = tk.Label(self.reg_frame, text="Password", font=("Helvetica", 12))
        self.reg_password_label.grid(row=4, column=0)
        self.reg_password = tk.Entry(self.reg_frame, show="*", font=("Helvetica", 12))
        self.reg_password.grid(row=4, column=1)

        self.reg_confirm_password_label = tk.Label(self.reg_frame, text="Confirm Password", font=("Helvetica", 12))
        self.reg_confirm_password_label.grid(row=5, column=0)
        self.reg_confirm_password = tk.Entry(self.reg_frame, show="*", font=("Helvetica", 12))
        self.reg_confirm_password.grid(row=5, column=1)

        self.reg_city_label = tk.Label(self.reg_frame, text="City", font=("Helvetica", 12))
        self.reg_city_label.grid(row=6, column=0)
        self.reg_city = tk.Entry(self.reg_frame, show="*", font=("Helvetica", 12))
        self.reg_city.grid(row=6, column=1)

        self.button_frame = tk.Frame(self.reg_frame)
        self.button_frame.grid(row=7, column=0, columnspan=2)

        self.register_button = tk.Button(self.button_frame, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_button.grid(row=0, column=0, padx=5)

        self.go_back_button = tk.Button(self.button_frame, text="Go back to login page", command=self.go_back_to_login, font=("Helvetica", 12))
        self.go_back_button.grid(row=0, column=1, padx=5)

    def register(self):
        username = self.reg_username.get()
        email = self.reg_email.get()
        password = self.reg_password.get()
        confirm_password = self.reg_confirm_password.get()
        phone = self.reg_phone.get()
        city = self.reg_city.get()

        if "@" not in email or email.count("@") != 1:
            messagebox.showerror("Error", "Invalid email format.")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return
        if not username or not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return
        if password == confirm_password:
            messagebox.showinfo("Registration Successful", f"Registration successful for {username} with email {email}.")
            salt = self.generate_salt()
            hashed_password = self.hash_password(password,salt)
            db.insert_or_delete_data(User.register(
                username,email,phone,salt,hashed_password,city
            ))
            self.go_back_to_login()
        else:
            messagebox.showerror("Registration Error", "Password confirmation does not match.")

    def go_back_to_login(self):
        self.root.destroy()
        from log import Login
        log_page = Login()
        log_page.run()

    def generate_salt(self):
        characters = string.ascii_letters + string.digits
        salt = ''.join(random.choice(characters) for _ in range(16))
        return salt

    def hash_password(self,password, salt):
        password_salt = salt + password
        hashed_password = hashlib.md5(password_salt.encode()).hexdigest()
        return hashed_password

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    register_page = Register()
    register_page.run()
