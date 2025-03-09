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
from datetime import datetime, timedelta

def createOrder(user_id,bike_id,start_time,from_X,from_Y,city,end_time,cost,to_X,to_Y):
    data = """
    INSERT INTO "order" (user_id, bike_id, start_date, from_X, from_Y,city,end_date,cost,to_X,to_Y)
    VALUES ({}, {}, \'{}\', {}, {},\'{}\',\'{}\',{},{},{})
    """.format(user_id,bike_id,start_time,from_X,from_Y,city,end_time,cost,to_X,to_Y)
    print(data)
    db.insert_or_delete_data(data)
def getXY(id):
    r = db.query_data(Bike.getBikeById(id))
    return r[0]['X'],r[0]['Y']
def generate_new_coordinates(X, Y, a):
    random_offset_X = random.randint(-a, a)
    random_offset_Y = random.randint(-a, a)
    new_X = max(0, X + random_offset_X)
    new_Y = max(0, Y + random_offset_Y)
    return new_X, new_Y
def generate_random_integer(a, b):
    if a > b:
        a, b = b, a
    random_integer = random.randint(a, b)
    return random_integer

def generate_random_times():
    start_date_A = datetime(2023, 9, 15)
    end_date_A = datetime(2023, 10, 22)
    random_time_A = timedelta(days=random.randint(0, (end_date_A - start_date_A).days),
                              minutes=random.randint(0, 100))
    random_datetime_A = start_date_A + random_time_A
    random_datetime_B = random_datetime_A + timedelta(minutes=random.randint(1, 100))
    formatted_time_A = random_datetime_A.strftime("%Y-%m-%d %H:%M:%S")
    formatted_time_B = random_datetime_B.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time_A, formatted_time_B

def generate_C_value(time_A, time_B,rate):
    time_format = "%Y-%m-%d %H:%M:%S"
    time_A = datetime.strptime(time_A, time_format)
    time_B = datetime.strptime(time_B, time_format)
    time_difference = time_B - time_A
    minutes_difference = time_difference.total_seconds() / 60  # 差值的分钟数
    C = 0
    while minutes_difference >= 30:
        C += rate
        minutes_difference -= 30
    return C+rate
# user 格拉斯哥 9-18,爱丁堡 19-28，阿伯丁 29-38，邓迪 39-48
# bike 格拉斯哥 5-24 bike 25-34 car
#      爱丁堡  35-51 bike 52-68 car
#      阿伯丁 69-78 bike  79-88 car
#      邓迪  89-98 bike 99-108 car
d = 100
rate = 5
city = "Dundee"
for i in range(10):
    user_id = generate_random_integer(39,48)
    bike_id = generate_random_integer(99,108)
    to_X,to_Y = getXY(bike_id)
    from_X,from_Y = generate_new_coordinates(to_X,to_Y,d)  ##20 for bike
    start_time,end_time = generate_random_times()
    cost = generate_C_value(start_time,end_time,rate)
    createOrder(user_id,bike_id,start_time,from_X,from_Y,city,end_time,cost,to_X,to_Y)


