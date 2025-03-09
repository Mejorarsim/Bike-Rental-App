import sqlite3
def get_connect():                  # To connect with the database_old
    return sqlite3.connect("db\database.db")

def query_data(sql):        # This method means to search the data from db, return with list with dict element
    database = get_connect()
    try:
        cursor = database.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        database.close()

def insert_or_delete_data(sql):
    database = get_connect()
    try:
        cursor = database.cursor()
        cursor.execute(sql)
        database.commit()
    finally:
        database.close()
