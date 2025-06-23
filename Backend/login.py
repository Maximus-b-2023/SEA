import sqlite3
import os


def login(email,password):
    try:
        conn = sqlite3.connect('./Database/tables.db')
        cur = conn.cursor()
    except:
        return "connection failed"
    try:
        sql = '''SELECT ROWID, USERNAME from user WHERE EMAIL = (?) AND PASSWORD = (?)'''
        params = (email, password)
        cur.execute(sql,params)
        creds = cur.fetchall()
        return int(creds)
    except:
        print("invalid email or password")
        return "invalid email or password"

def getUsername(UID):
    try:
        conn = sqlite3.connect('./Database/tables.db')
        cur = conn.cursor()
    except:
        return "connection failed"
    try:
        sql = '''SELECT USERNAME FROM user WHERE ROWID = (?)'''
        params = (UID,)
        cur.execute(sql,params)
        username = cur.fetchone()
        return username[0]
    except:
        print("Username retrieval failed")
        return "Username retrieval failed"
