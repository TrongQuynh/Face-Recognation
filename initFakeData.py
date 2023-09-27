from datetime import datetime, date
import os
import random
from Query import Query
from model.Employee import Employee
from calendar import monthrange

# Query().insert_Account()


def randomPhoneNumber():
    result = "09"
    for i in range(8):
        random_num = random.randint(0, 9)
        result = result + str(random_num)
    return result


def randomDepartment():
    departments = Query().select_All_Department()
    index = random.randrange(0, len(departments))
    return (departments[index])[0]


def createEmployee(dataset):
    e_name = dataset.split("-")[0]
    email = f"{e_name}@gmail.com"
    phonenumber = str(randomPhoneNumber())
    departmentID = randomDepartment()
    e = Employee(e_name, email, phonenumber, dataset, departmentID)
    print(f"{e_name}-{email}-{phonenumber}-{departmentID}")
    Query().insert_Employee(e)


def initFakeEmployeeData():
    path_dataset = "./data/dataset/"
    for folder in os.listdir(f"{path_dataset}"):
        createEmployee(folder)

# ======================================================================
# ==================== Create Fake Timekeeping data =====================


def randomTime(isTimein):
    hours = random.randint(13, 20)
    if (isTimein):
        hours = random.randint(6, 12)
    minute = random.randint(0, 59)
    seconnds = random.randint(0, 59)
    return datetime.strptime(f"{hours}:{minute}:{seconnds}", "%H:%M:%S")


def createTKR(employee):
    current_month = datetime.today().month
    curent_year = datetime.today().year

    start_month = 8
    end_month = 12  # 11

    for month in range(start_month, int(end_month)):
        number_day_of_month = monthrange(int(curent_year), int(month))[1]
        for day in range(1, number_day_of_month + 1):
            datetimeInstance = datetime(int(curent_year), int(month), int(day))

            employee_ID = employee[0]
            dateInstance = datetimeInstance.date()
            time_in = randomTime(True)
            time_out = randomTime(False)
            Query().insert_Timekeeping_Record_2(employee_ID, dateInstance, time_in, time_out)
    print(
        f"Number day of {month}: {monthrange(int(curent_year),int(month))}")


def initFakeTKRData():
    current_month = datetime.today().month
    curent_year = datetime.today().year

    for employee in Query().select_All_Employee():
        createTKR(employee)


# initFakeTKRData()
