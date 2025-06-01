import sqlite3

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
        '''INSERT INTO user (USERNAME,PASSWORD,EMAIL,ACCOUNTTYPE)
        VALUES
            ("TestUser1","Test1","TestUser1@email.com","Admin"),
            ("TestUser2","Test2","TestUser2@email.com","User"),
            ("TestUser3","Test3","TestUser3@email.com","User"),
            ("TestUser4","Test4","TestUser4@email.com","User"),
            ("TestUser5","Test5","TestUser5@email.com","User");'''
        )
        conn.commit()
        print("Insert success")
    except: print("insert failed")
        
mockCrops()
mockUsers()
