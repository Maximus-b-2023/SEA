import sqlite3

try:
    conn = sqlite3.connect('./Database/tables.db')
    cur = conn.cursor()
except:
    print("connection failed")

def authAdmin(UID):
    try:
        sql = '''SELECT ACCOUNTTYPE FROM user WHERE ROWID = ''' + str(UID) + ';'
        cur.execute(sql)
        accountType = cur.fetchone()
    except:
        print("retrieval failed")
        return "retrival failed"
    if str(accountType[0]) == "Admin":
        print("True")
        return True
    else:
        print("False")
        return False


def fetchUsers(UID):
    if authAdmin(UID) == True:
        try:
            sql = '''SELECT ROWID, USERNAME, ACCOUNTTYPE FROM user'''
            cur.execute(sql)
            userList = cur.fetchall()
            print(userList)
            return userList
        except:
            print("Fetch failed")
            return "Fetch failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"
    

def updateAccountType(UID,targetUID, newAccountType):
    if authAdmin(UID) == True:
        try:
            sql = '''UPDATE user SET ACCOUNTTYPE = "''' + newAccountType + '" WHERE ROWID = ' + str(targetUID) + ';'
            conn.execute(sql)
            conn.commit()
            print ("User " + str(targetUID) + " updated to account type " + newAccountType)
            return ("User " + str(targetUID) + " updated to account type " + newAccountType)
        except:
            print("Update failed")
            return "Update failed"
    else:
        print("User not verified for this action")
        return "User not verified for this action"

