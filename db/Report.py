# Packaged sql sentences dealing with User Tables

def createReport(user_id,order_id,bike_id,message,problem_type,date,city):
    data = """
    INSERT INTO report (user_id, order_id, bike_id, message, problem_type, is_solved, city, date)
    VALUES ({}, {}, {}, \'{}\', \'{}\', 0, \'{}\', \'{}\')
    """.format(user_id,order_id,bike_id,message,problem_type,city,date)
    return data

def getReportByOrderId(id):
    return 'select * from report where order_id = {}'.format(id)

def getReportByUserId(user_id):
    return 'select * from report where user_id = {}'.format(user_id)

def getAllReport(city):
    return 'select * from report where city = \'{}\''.format(city)

def getReportByStatus(status,city):
    x= 0
    if status=='Done':
        x = 1
    elif status=='Unfinished':
        x = 0
    return 'select * from report where is_solved = {} and city = \'{}\''.format(x,city)

def getReportByStatusAndUserId(status,user_id):
    x= 0
    if status=='Done':
        x = 1
    elif status=='Unfinished':
        x = 0
    return 'select * from report where is_solved = {} and user_id = {}'.format(x,user_id)

def doneReport(id):
    return 'update report set is_solved = 1 where id = {}'.format(id)