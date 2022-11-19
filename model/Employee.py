import db


class Employee:

    def __init__(self, fullname, email, phonenumber, dataset, department_id=None) -> None:
        self.fullname = fullname
        self.email = email
        self.phonenumber = phonenumber
        self.dataset = dataset
        self.department_id = department_id

    def show_Employee_info(self):
        print(self.fullname + "\n" + self.email + "\n" +
              self.phonenumber + "\n" + self.dataset + "\n" + self.department_id)

    # Query
    def insert_new_employee(self):
        mydb = db.connectDB()
        mycursor = mydb.cursor()
        sql_query = "INSERT INTO Employee (fullname, phonenumber,email,datase,department_id) VALUES (%s, %s,%s, %s, %s)"
        values = (self.fullname, self.email,
                  self.phonenumber, self.dataset, self.department_id)
        mycursor.execute(sql_query, values)
        mydb.commit()
        print(mycursor.rowcount, "new employee inserted.")
