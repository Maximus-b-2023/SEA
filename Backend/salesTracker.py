import sqlite3

from costCalculators import calcSeedCost

try:
    conn = sqlite3.connect('./Database/tables.db')
except:
    print("connection failed")

def createSaleReport(userId,cropName, season, quantity, revenue):
    profit = revenue - calcSeedCost(cropName, quantity)
    sql = '''INSERT INTO sales (USERID,CROPNAME,SEASON,QUANTITYSOLD,PROFITMADE)
        VALUES
            ('''+ str(userId) + ',"'+ cropName + '","'+ season + '",' + str(quantity) + ',' + str(profit) + ');'
    try:
        conn.execute(sql)
        conn.commit()
        print("Insert successful")
        return("insert successful")
    except:
        print("insert failed - "+ sql)
        return "insert successful"

createSaleReport(2,"Strawberry","Spring",200,40000)