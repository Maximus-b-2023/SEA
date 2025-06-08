import sqlite3


def signup(username,password,email):
    try:
        conn = sqlite3.connect('./Database/tables.db')
    except:
        return "connection failed"
    sql = '''INSERT INTO user (USERNAME,PASSWORD,EMAIL,ACCOUNTTYPE) VALUES(?,?,?,?)''' 
    params = (username, password, email, "User")
    try:
        conn.execute(sql,params)
        conn.commit()
    except:
        return "insert failed " + str(sql)
    return "user successfully created"

