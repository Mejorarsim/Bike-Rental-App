# Packaged sql sentences dealing with User Tables
# TODO...

def createBike(X,Y,type,city):
    data = """
    INSERT INTO bike (X,Y,bike_type,city,is_broken,is_use,total_minutes,battery)
    VALUES ({}, {}, \'{}\',\'{}\',0,-1,0,100)
    """.format(X,Y,type,city)
    return data
def getBikeById(bike_id):
    return 'select * from bike where id = {}'.format(bike_id)

def deleteBikeById(bike_id):
    return 'delete from bike where id = {}'.format(bike_id)
def getUserByBikeId(bike_id):
    return 'select is_use from bike where id = {}'.format(bike_id)
def getAllBike(city):
    return 'select * from bike where city = \'{}\''.format(city)

def fix(id):
    return 'update bike set is_broken = 0 where id = {}'.format(id)

def broken(id):
    return 'update bike set is_broken = 1 where id = {}'.format(id)

def changeBattery(id):
    return 'update bike set battery = 100 where id = {}'.format(id)

def getBikeByTypes(bike_type,city):
    return 'select * from bike where bike_type = \'{}\' and city = \'{}\''.format(bike_type,city)

def getColorForBike(type):
    dict = {'Bike':'red','Car':'blue'}
    return dict[type]

def findIsUse(user_id):
    return 'select * from bike where is_use = {}'.format(user_id)

def ownBike(user_id,id):
    return 'update bike set is_use = {} where id = {}'.format(user_id,id)
def returnBike(id):
    return 'update bike set is_use = -1 where id = {}'.format(id)
def lowBattery(id,battery):
    return 'update bike set battery = {} where id = {}'.format(battery,id)
def changelocation(id,X,Y):
    return 'update bike set X = {}, Y = {} where id = {}'.format(X,Y,id)

def addMinutes(id,minutes):
    return 'update bike set total_minutes = total_minutes + {} where id = {}'.format(minutes,id)