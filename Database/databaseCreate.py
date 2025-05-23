import sqlite3

def createUserTable():
    conn = sqlite3.connect('./Database/user.db')

    conn.execute('''CREATE TABLE user
                 (ID INT PRIMARY KEY     NOT NULL,
                 USERNAME       TEXT    NOT NULL,
                 PASSWORD       TEXT    NOT NULL,
                 EMAIL          TEXT    NOT NULL);''')
    print("Table Created successfully")

createUserTable()