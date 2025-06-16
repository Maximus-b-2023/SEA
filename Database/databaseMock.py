import sqlite3

def updateAccountType(targetUID, newAccountType):
    try:
        conn = sqlite3.connect('./Database/tables.db')
        cur = conn.cursor()
    except:
        return "connection failed"
    #if authAdmin(UID) == True:
    try:
        sql = '''UPDATE users SET accounttype = "''' + newAccountType + '" WHERE ROWID = ' + str(targetUID) + ';'
        conn.execute(sql)
        conn.commit()
        print ("User " + str(targetUID) + " updated to account type " + newAccountType)
        return ("User " + str(targetUID) + " updated to account type " + newAccountType)
    except:
        print("Update failed")
        return "Update failed"
    #else:
        print("User not verified for this action")
        return "User not verified for this action"

conn = sqlite3.connect('./Database/tables.db')
cur = conn.cursor

def mockCrops():
    try:
        conn.execute(
        '''INSERT INTO crops (CROPNAME,SEEDPRICE,LOWESTSELLINGPRICE)
        VALUES
            ("Blue Jazz",30,50),
            ("Cauliflower",80,175),
            ("Garlic",40,60),
            ("Green Bean",60,40),
            ("Kale",70,110),
            ("Parsnip",70,110),
            ("Potato",50,80),
            ("Strawberry",100,120),
            ("Tulip",20,30),
            ("Unmilled Rice",40,30);'''
        )
        conn.commit()
        print("Insert success")
    except: print("insert failed")

def mockUsers():
    try:
        conn.execute(
        '''INSERT INTO users (username,password,email,accounttype)
        VALUES
            ("TestUser1","pbkdf2:sha256:1000000$csl2VrHnTowjV2Sv$465562343bd7ca7160580d75f02e2eb3e61940ea2626bc6eb31f6a6d9b729485","TestUser1@email.com","Admin"),
            ("TestUser2","pbkdf2:sha256:1000000$J3LhzEqa5hflvj7L$526ee2f1bdee613ef8c729c5ccafb257c5e4ec4b6026307dcb48e6b37c0dc9fd","TestUser2@email.com","User"),
            ("TestUser3","pbkdf2:sha256:1000000$J3LhzEqa5hflvj7L$526ee2f1bdee613ef8c729c5ccafb257c5e4ec4b6026307dcb48e6b37c0dc9fd","TestUser3@email.com","User"),
            ("TestUser4","pbkdf2:sha256:1000000$J3LhzEqa5hflvj7L$526ee2f1bdee613ef8c729c5ccafb257c5e4ec4b6026307dcb48e6b37c0dc9fd","TestUser4@email.com","User"),
            ("TestUser5","pbkdf2:sha256:1000000$J3LhzEqa5hflvj7L$526ee2f1bdee613ef8c729c5ccafb257c5e4ec4b6026307dcb48e6b37c0dc9fd","TestUser5@email.com","User");'''
        )
        conn.commit()
        print("Insert success")
    except: print("insert failed")

def setAdmin(UID,AccountType):
    try:
        updateAccountType(UID, AccountType)
        print("Update success")
    except:
        print("Update failed")
        
# mockCrops()
# mockUsers()
setAdmin(1, "Admin")
