import sqlite3

from costCalculators import calcSeedCost


def createSaleReport(userId,cropName, season, quantity, revenue):
    try:
        conn = sqlite3.connect('./Database/tables.db')
    except:
        return "connection failed"
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