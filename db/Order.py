# Packaged sql sentences dealing with User Tables
# TODO...
def startOrder(user_id,bike_id,start_time,from_X,from_Y,city):
    data = """
    INSERT INTO "order" (user_id, bike_id, start_date, from_X, from_Y,city)
    VALUES ({}, {}, \'{}\', {}, {},\'{}\')
    """.format(user_id,bike_id,start_time,from_X,from_Y,city)
    return data

def endOrder(id,end_time,to_X,to_Y,cost):
    return 'update "order" set end_date = \'{}\', to_X = {}, to_Y = {}, cost = {} where id = {}'.format(
        end_time,to_X,to_Y,cost,id
    )
def getUnfinishedOrder(user_id):
    return 'select * from "order" where user_id = {} and end_date is NULL'.format(user_id)
def getOrder(id):
    return 'select * from "order" where id = {}'.format(id)

def getUserOrder(user_id):
    return 'select * from "order" where user_id = {}'.format(user_id)