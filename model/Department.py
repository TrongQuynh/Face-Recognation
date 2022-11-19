import db


class Department:
    def __init__(self, department_name) -> None:
        self.department_name = department_name

    def insert_new_department(self):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Department (department_name) VALUES (%s)"
        values = (self.department_name,)
        mycursor.execute(sql_query, values)
        mydb.commit()
