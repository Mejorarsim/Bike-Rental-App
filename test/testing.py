import sqlite3
import db.db_config as db
import db.Bike as Bike
import db.Order as Order
import db.Report as Report
import db.User as User
import tkinter as tk
import hashlib
import random
import string
import random
def generate_random_name():
    name_length = random.randint(3, 6)
    first_letter = random.choice(string.ascii_uppercase)
    rest_letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(name_length - 1))
    random_name = first_letter + rest_letters
    return random_name
def generate_random_email():
    email_prefix = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(1, 5)))
    email = f"{email_prefix}@qq.com"
    return email
def generate_random_phone_number():
    phone_number = ''.join(random.choice("0123456789") for _ in range(10))
    return phone_number
def generate_salt():
    characters = string.ascii_letters + string.digits
    salt = ''.join(random.choice(characters) for _ in range(16))
    return salt
def hash_password(password, salt):
    password_salt = salt + password
    hashed_password = hashlib.md5(password_salt.encode()).hexdigest()
    return hashed_password
def generate_random_float():
    random_float = round(random.uniform(0, 100), 2)
    return random_float
dict = ["Glasgow","Edinburgh","Aberdeen","Dundee"]
for city in dict:
    for i in range(10):
        username = generate_random_name()
        email = generate_random_email()
        phone =generate_random_phone_number()
        salt=generate_salt()
        password_origin= "123456"
        password = hash_password(password_origin,salt)
        wallet = generate_random_float()
        sql = """
        INSERT INTO user (user_name, email, phone, salt, password, wallet, city, user_type)
        VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\', 'User')
        """.format(username,email,phone,salt,password,wallet,city)
        db.insert_or_delete_data(sql)