import sqlite3

def createUserTable():
    conn = sqlite3.connect('./Database/tables.db')

    conn.execute('''CREATE TABLE user
                 (USERNAME       TEXT    NOT NULL,
                 PASSWORD       TEXT    NOT NULL,
                 EMAIL          TEXT    NOT NULL);''')
    print("Table Created successfully")

def createCropsTable():
    conn = sqlite3.connect('./Database/tables.db')

    conn.execute('''CREATE TABLE crops
                 (CROPNAME       TEXT    NOT NULL,
                 SEEDPRICE       INT    NOT NULL,
                 LOWESTSELLINGPRICE          INT    NOT NULL);''')
    print("Table Created successfully")

def createSalesTable():
    conn = sqlite3.connect('./Database/tables.db')

    conn.execute('''CREATE TABLE sales
                 (USERID         TEXT   NOT NULL,
                 CROPNAME       TEXT    NOT NULL,
                 SEASON         TEXT    NOT NULL,
                 QUANTITYSOLD          TEXT    NOT NULL,
                 PROFITMADE     INT     NOT NULL,
                 FOREIGN KEY(USERID) REFERENCES user(ROWID));''')
    print("Table Created successfully")

createUserTable()
createCropsTable()
createSalesTable()