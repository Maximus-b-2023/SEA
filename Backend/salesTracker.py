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
    except:
        print("insert failed - "+ sql)

createSaleReport(1,"Strawberry","Spring",200,30000)