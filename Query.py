
import db
from Employee import Employee
from Time_KP_Recoed import TimekeepingRecord


class Query():
    def __init__(self) -> None:
        self.mydb = db.connectDB()
        self.cursor = self.mydb.cursor()

        # TEST BRANCH

    def insert_Employee(self, employee):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Employee (fullname, phonenumber,email,dataset) VALUES (%s, %s,%s, %s)"
        values = (employee.fullname, employee.email,
                  employee.phonenumber, employee.dataset)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    def insert_Timekeeping_Record(self, T_record):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Timekeeping_Record (employee_id,date, time_in,time_out) VALUES (%s, %s,%s, %s)"
        values = (T_record.e_id, T_record.date, T_record.time_in,
                  T_record.time_out)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "record inserted Timekeeping.")

    def update_Timekeeping_Record(self, e_id):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "UPDATE Timekeeping_Record SET time_out = %s WHERE id = %s"
        values = (TimekeepingRecord.get_datetime_now(), e_id)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "Update Timekeeping success")

    def select_Employee_by_ID(self, e_id):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Employee WHERE id = %s"
        values = (e_id,)
        mycursor.execute(sql_query, values)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchone()
        print(myresult)
        return myresult

    def select_All_Employee(self):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Employee"

        mycursor.execute(sql_query)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchall()
        print("--- Data all employee ---")
        # print(myresult)
        return myresult


query = Query()
employee_1 = Employee("Phong", "abc@gmail.com", "0934234234", "/data/Quynh")
timekeeping_1 = TimekeepingRecord(e_id=1)
# query.insert_Employee(employee_1)
# query.insert_Timekeeping_Record(timekeeping_1)
# query.select_Employee_by_ID(1)
query.update_Timekeeping_Record(1)
