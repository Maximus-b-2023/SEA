import sqlite3

try:
    conn = sqlite3.connect('./Database/tables.db')
    cur = conn.cursor()
except:
    print("connection failed")


def login(email,password):
    try:
        sql = '''SELECT ROWID from user WHERE EMAIL = "''' + email + '''" AND PASSWORD = "''' + password + '";'
        cur.execute(sql)
        UID = cur.fetchone()
        print(int(UID[0]))
        return int(UID[0])
    except:
        print("invalid email or password")
        return "invalid email or password"
    
login("TestUser2@email.com", "Test2")
     
