import sqlite3

conn = sqlite3.connect('./Database/tables.db')
cur = conn.cursor()

def getCropPrice(userinput):
    sql = 'select LOWESTSELLINGPRICE from crops WHERE CROPNAME ="'+ userinput + '";'
    cur.execute(sql)
    cropPrice = cur.fetchone()
    return int(cropPrice[0])

getCropPrice('Strawberry')

def calcMinValue(cropName, quantity):
    minValue = quantity * getCropPrice(cropName)
    return minValue

print(calcMinValue("Strawberry", 20))