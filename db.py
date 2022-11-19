import mysql.connector


def connectDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="van phong54664",
        database="timekeeping"
    )
    return mydb
