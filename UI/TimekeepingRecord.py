from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtCore import QRect, QPropertyAnimation
from threading import Thread
from Query import Query


class Timekeeping_Record(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/TimekeepingRecord.ui", self)
        self.center()
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))
        self.intit_table()

        self.departments = None
        self.employees = None

        self.tbl_Department.cellClicked.connect(self.event_choose_department)
        self.tbl_Employee.cellClicked.connect(self.event_choose_employee)

        self.btn_Search_Department.clicked.connect(
            self.event_search_department)
        self.btn_Search_Employee.clicked.connect(self.event_search_employee)

    def init_form(self):
        self.departments = Query().select_All_Department()
        self.load_data_table_department(self.departments)
        self.init_throughScreenText()

    def init_throughScreenText(self):
        self.label_Text.setText("HUTECH INSTITUTE of INTERNATIONAL EDUCATION")
        self.setStyleSheet("#label_Text{color : yellow}")
        self.label_Text.move(-30, 680)
        self.loopCount = 100
        self.doAnim()

    def doAnim(self):

        self.anim = QPropertyAnimation(self.label_Text, b"geometry")
        # self.anim = QPropertyAnimation(self.frame, b"geometry")

        self.anim.setDuration(10000)
        self.anim.setStartValue(QRect(-400, 740, 400, 30))
        self.anim.setEndValue(QRect(1700, 740, 400, 30))
        self.anim.setLoopCount(self.loopCount)
        self.anim.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def intit_table(self):
        # Remove index of table
        self.tbl_Employee.verticalHeader().setVisible(False)
        self.tbl_Department.verticalHeader().setVisible(False)
        self.tbl_Timekeeping.verticalHeader().setVisible(False)

        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Department.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Timekeeping.setSelectionBehavior(QTableView.SelectRows)

        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 200)
        self.tbl_Employee.setColumnWidth(2, 200)
        self.tbl_Employee.setColumnWidth(3, 200)
        self.tbl_Employee.setColumnWidth(4, 50)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number"])

        self.tbl_Department.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Department.setColumnWidth(0, 50)
        self.tbl_Department.setColumnWidth(1, 219)
        self.tbl_Department.setColumnWidth(2, 100)
        self.tbl_Department.setHorizontalHeaderLabels(
            ["ID", "Department name", "Total"])

    def load_data_table_department(self, departments):
        self.tbl_Department.setRowCount(len(departments))
        table_row = 0
        for d in departments:
            print(d)
            total_employee = len(
                Query().select_Employee_by_department_ID(int(d[0])))
            self.tbl_Department.setItem(
                table_row, 0, QTableWidgetItem(str(d[0])))
            self.tbl_Department.setItem(table_row, 1, QTableWidgetItem(d[1]))
            self.tbl_Department.setItem(
                table_row, 2, QTableWidgetItem(str(total_employee)))

            table_row += 1

        self.lbl_Department.setText(
            f"Total Department: {str(len(self.departments))}")

    def load_data_table_employee(self, employees):
        if (len(employees) < 1):
            print("Notification: Not found employee")
        self.tbl_Employee.setRowCount(len(employees))
        table_row = 0
        for e in employees:
            self.tbl_Employee.setItem(
                table_row, 0, QTableWidgetItem(str(e[0])))
            self.tbl_Employee.setItem(
                table_row, 1, QTableWidgetItem(str(e[1])))
            self.tbl_Employee.setItem(
                table_row, 2, QTableWidgetItem(str(e[2])))
            self.tbl_Employee.setItem(
                table_row, 3, QTableWidgetItem(str(e[3])))
            self.tbl_Employee.setItem(
                table_row, 4, QTableWidgetItem(str("ON")))
            table_row += 1

        self.lbl_Employee.setText(
            f"Total Employee: {str(len(employees))}")

    def load_data_table_TKRecord(self, data_record):
        self.tbl_Timekeeping.setRowCount(len(data_record))
        table_row = 0
        for r in data_record:

            self.tbl_Timekeeping.setItem(
                table_row, 0, QTableWidgetItem(str(r[1])))
            self.tbl_Timekeeping.setItem(
                table_row, 1, QTableWidgetItem(str(r[2])))
            time_out = r[3]
            if (r[3] == None):
                time_out = ""
            self.tbl_Timekeeping.setItem(
                table_row, 2, QTableWidgetItem(str(time_out)))

    # Helper
    def is_number(self, number):
        try:
            int(number)
            return True
        except:
            return False

    # Event
    def event_choose_department(self, row, col):
        department_ID = self.tbl_Department.item(row, 0).text()

        self.employees = Query().select_Employee_by_department_ID(department_ID)
        # [(19, 'Nong Trong Quynh', 'abc@gmail.com', '093866522341', 'NongTrongQuynh-1668816362', 1)]
        self.load_data_table_employee(self.employees)

    def event_choose_employee(self, row, col):
        employee_ID = self.tbl_Employee.item(row, 0).text()
        record_data = Query().select_All_TKRecord_by_EmployeeID(int(employee_ID))
        # (2, datetime.date(2022, 2, 15), datetime.timedelta(seconds=36863), None, 19)
        self.load_data_table_TKRecord(record_data)

    def event_search_employee(self, *arg, **kwargs):
        current_department_row = self.tbl_Department.currentRow()
        if (current_department_row < 0):
            print("Notification: Please choose department")
            return
        total_employee_row = self.tbl_Employee.rowCount()
        # if (total_employee_row < 1):
        #     print("Notification: Not have employee in this department")
        #     return
        employee_list = []
        text_search = self.txt_Search_Employee.text()
        if (self.is_number(text_search)):
            for e in self.employees:
                if e[0] == int(text_search):
                    employee_list.append(e)
            self.load_data_table_employee(employee_list)
        else:
            for e in self.employees:
                e_FName = str(e[1]).replace(" ", "").lower()
                search_FName = str(text_search).replace(" ", "").lower()
                if search_FName in e_FName or e_FName in search_FName:
                    employee_list.append(e)
            self.load_data_table_employee(employee_list)

    def event_search_department(self):
        txt_search = self.txt_Search_Department.text()
        departments = []
        if (len(str(txt_search)) < 1):
            departments = Query().select_All_Department()
            self.load_data_table_department(departments)
            return

        if (self.is_number(txt_search)):
            department = Query().select_Department_by_ID(int(txt_search))
            departments.append(department)
            self.load_data_table_department(departments)
        else:
            for d in Query().select_All_Department():

                if (str(d[1]).lower().replace(" ", "") in str(txt_search).lower() or str(txt_search).lower() in str(d[1]).lower().replace(" ", "")):
                    departments.append(d)
            self.load_data_table_department(departments)
