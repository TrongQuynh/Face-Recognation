from datetime import datetime, date
import db


class TimekeepingRecord:
    def __init__(self, e_id) -> None:
        self.e_id = e_id
        self.date = date.today()
        self.time_in = datetime.now()
        self.time_out = None

    def get_datetime_now():
        return datetime.now()

    def get_time_now(self):
        return datetime.now().strftime("%H:%M:%S")

    def show_info(self):
        print("Employee ID: " + self.e_id+"\nTime: " + self.date + "\n" + "Time in: " +
              self.time_in + "\n" + "Time out: " + self.time_out)

    def insert_Timekeeping_Record(self):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Timekeeping_Record (employee_id,date, time_in,time_out) VALUES (%s, %s,%s, %s)"
        values = (self.e_id, self.date, self.time_in,
                  self.time_out)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "new Timekeeping inserted.")

    def update_Timekeeping_Record(self, e_id):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "UPDATE Timekeeping_Record SET time_out = %s WHERE id = %s"
        values = (TimekeepingRecord.get_datetime_now(), e_id)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "Update Timekeeping success")
