
import db
from model.Employee import Employee
from model.Time_KP_Recoed import TimekeepingRecord
from model.Department import Department
from datetime import datetime, date


class Query():
    def __init__(self) -> None:
        pass

    # Employee
    def insert_Employee(self, employee):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Employee (fullname,email,phonenumber,dataset,department_id) VALUES (%s, %s,%s, %s, %s)"
        values = (employee.fullname, employee.email,
                  employee.phonenumber, employee.dataset, employee.department_id)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    def select_Employee_by_ID(self, e_id):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Employee WHERE id = %s"
        values = (e_id,)
        mycursor.execute(sql_query, values)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchone()
        # print(myresult)
        return myresult

    def select_Employee_by_dataset(self, dataset):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Employee WHERE dataset = %s"
        values = (dataset,)
        mycursor.execute(sql_query, values)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchone()
        # print(myresult)
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

    def select_Employee_by_department_ID(self, department_ID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Employee WHERE department_id = %s"
        values = (department_ID,)
        mycursor.execute(sql_query, values)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchall()
        # print(myresult)
        return myresult

    def delete_Employee_by_ID(self, employee_ID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "DELETE FROM Employee WHERE id = %s"
        values = (employee_ID,)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print("Delete employee: " + str(employee_ID) + " Successfull")

    def update_Employee_by_ID(self, employee, employeeID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "UPDATE Employee SET fullname = %s,email= %s,phonenumber= %s,dataset= %s,department_id= %s WHERE id = %s"
        values = (employee.fullname, employee.email, employee.phonenumber,
                  employee.dataset, employee.department_id, employeeID)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, f"Update Employee {employeeID} success")

    def update_Department_of_Employee(self, employee_ID, department_ID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "UPDATE Employee SET department_id= %s WHERE id = %s"
        values = (department_ID, employee_ID)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print("Update department for employee success")
    # Timekeeping Record

    def select_All_TKRecord_by_EmployeeID(self, employee_ID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Timekeeping WHERE employee_id = %s"
        values = (employee_ID,)
        mycursor.execute(sql_query, values)
        myresult = mycursor.fetchall()
        return myresult

    def select_All_TKRecord_in_range(self, date_1, date_2):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Timekeeping WHERE date BETWEEN %s AND %s"
        values = (date_1, date_2)
        mycursor.execute(sql_query, values)
        myresult = mycursor.fetchall()
        return myresult

    def select_All_TKRecord_by_EmployeeID_and_Date(self, employee_ID, date):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Timekeeping WHERE employee_id = %s AND date = %s"
        values = (employee_ID, date)
        mycursor.execute(sql_query, values)
        myresult = mycursor.fetchone()
        return myresult

    def insert_Timekeeping_Record(self, T_record):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Timekeeping (employee_id,date, time_in,time_out) VALUES (%s, %s,%s, %s)"
        values = (T_record.e_id, T_record.date, T_record.time_in,
                  T_record.time_out)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "record inserted Timekeeping.")

    def update_Timekeeping_Record(self, e_id, TR_id):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "UPDATE Timekeeping SET time_out = %s WHERE employee_id = %s AND id = %s"
        values = (datetime.now(), e_id, TR_id)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "Update Timekeeping success")

    def select_All_TKRecord_by_Date(self, date):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Timekeeping WHERE date = %s"
        values = (date,)
        mycursor.execute(sql_query, values)
        myresult = mycursor.fetchall()
        return myresult

    def delete_All_TKRecord_by_EmployeeID(self, employee_ID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "DELETE FROM Timekeeping WHERE employee_id = %s"
        values = (employee_ID,)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print("Delete all timekeeping record: " +
              str(employee_ID) + " Successfull")

    # Department
    def select_Department_by_Name(self, department_name):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Department WHERE department_name = %s"
        values = (department_name,)
        mycursor.execute(sql_query, values)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchone()
        return myresult

    def select_All_Department(self):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Department"
        mycursor.execute(sql_query)
        myresult = mycursor.fetchall()
        return myresult

    def select_Department_by_ID(self, department_ID):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "SELECT * FROM Department WHERE id = %s"
        values = (department_ID,)
        mycursor.execute(sql_query, values)
        # myresult = mycursor.fetchall()
        myresult = mycursor.fetchone()
        return myresult

    def insert_New_Department(self, department_name):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Department (department_name) VALUES (%s)"
        values = (department_name,)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "Insert new Department Success")


query = Query()
