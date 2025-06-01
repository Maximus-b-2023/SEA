import sqlite3

try:
    conn = sqlite3.connect('./Database/tables.db')
except:
    print("connection failed")

def signup(username,password,email):
    sql = '''INSERT INTO user (USERNAME,PASSWORD,EMAIL,ACCOUNTTYPE)
    VALUES ("''' + username + '","' + password + '","' + email + '","User");' 
    try:
        conn.execute(sql)
        conn.commit()
    except:
        return "insert failed " + sql
    return "user successfully created"

signup("TestUser6","Test6","TestUser6@email.com")

