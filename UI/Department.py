from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidgetItem, QTableView, QMessageBox
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtCore import QRect, QPropertyAnimation
from threading import Thread
from Query import Query
from datetime import datetime, date


class Department(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Department.ui", self)
        self.center()
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))
        # self.btn_Search.setPixmap(
        #     QPixmap("./public/img/search.png"))
        # self.btn_Search_2.setPixmap(
        #     QPixmap("./public/img/search.png"))
        self.intit_table()
        self.employees = None

        self.btn_CompleteUpdate.setEnabled(False)

        self.tbl_Department.cellClicked.connect(self.event_choose_department)
        self.btn_Search.clicked.connect(self.event_search_employee)
        self.btn_Search_2.clicked.connect(self.event_search_department)
        self.btn_ChangeDepartment.clicked.connect(self.event_Change_Department)

        self.btn_CreateDepartment.clicked.connect(self.event_create_Department)
        self.btn_CompleteUpdate.clicked.connect(self.event_complete_update)
        self.btn_Refresh.clicked.connect(self.event_refresh)

    def init_form(self):
        departments = Query().select_All_Department()
        self.load_data_table_department(departments)
        self.load_cbox_data()
        self.init_throughScreenText()
        self.isUpdateDepartment = False

    def load_cbox_data(self):
        # delete items of list
        self.cbox_Department.clear()

        # [(1, 'IT'), (2, 'Marketing')]
        departments = Query().select_All_Department()
        self.cbox_Department.addItem("None")
        for d in departments:
            self.cbox_Department.addItem(d[1])

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
        self.anim.setStartValue(QRect(-400, 730, 400, 30))
        self.anim.setEndValue(QRect(1700, 730, 400, 30))
        self.anim.setLoopCount(self.loopCount)
        self.anim.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def intit_table(self):
        # Remove index of table
        self.tbl_Department.verticalHeader().setVisible(False)
        self.tbl_Employee.verticalHeader().setVisible(False)

        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Department.setSelectionBehavior(QTableView.SelectRows)

        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 200)
        self.tbl_Employee.setColumnWidth(2, 200)
        self.tbl_Employee.setColumnWidth(3, 200)
        self.tbl_Employee.setColumnWidth(4, 50)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number", "Status"])

        self.tbl_Department.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Department.setColumnWidth(0, 40)
        self.tbl_Department.setColumnWidth(1, 170)
        self.tbl_Department.setColumnWidth(2, 80)
        self.tbl_Department.setHorizontalHeaderLabels(
            ["ID", "Department name", "Total"])

    def load_data_table_department(self, departments):

        self.tbl_Department.setRowCount(len(departments))
        table_row = 0
        for d in departments:
            total_employee = len(
                Query().select_Employee_by_department_ID(int(d[0])))
            self.tbl_Department.setItem(
                table_row, 0, QTableWidgetItem(str(d[0])))
            self.tbl_Department.setItem(table_row, 1, QTableWidgetItem(d[1]))
            self.tbl_Department.setItem(
                table_row, 2, QTableWidgetItem(str(total_employee)))

            table_row += 1

    def status_of_employee(self, e_ID):
        date_today = date.today()
        TR_id = Query().select_All_TKRecord_by_EmployeeID_and_Date(
            int(e_ID), date_today)
        return "ON" if TR_id else "OFF"

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

            status = str(self.status_of_employee(e[0]))
            color = QtGui.QColor(
                255, 0, 0) if status == "OFF" else QtGui.QColor(0, 255, 0)
            self.tbl_Employee.setItem(
                table_row, 4, QTableWidgetItem(status))
            self.tbl_Employee.item(table_row, 4).setBackground(color)
            table_row += 1
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

    def event_Change_Department(self):
        '''
            let employee join into other Department
            show all emploee in employee table
        '''

        self.isUpdateDepartment = not self.isUpdateDepartment
        self.btn_CreateDepartment.setEnabled(not self.isUpdateDepartment)
        self.btn_CompleteUpdate.setEnabled(self.isUpdateDepartment)
        if (self.isUpdateDepartment):
            employees = Query().select_All_Employee()
            self.load_data_table_employee(employees)
            pass
        else:
            self.load_data_table_employee([])

    def event_complete_update(self):
        if (not self.isUpdateDepartment):
            print("Please click Update employee")
            return
        rows = {index.row()
                for index in self.tbl_Employee.selectionModel().selectedIndexes()}
        if (self.cbox_Department.currentIndex() == 0):
            self.event_show_messageBox(
                "Warning validate!", "Notification: Please choose department")
            return
        if (len(rows) < 1):
            self.event_show_messageBox("Warning", "Please choose employee")
            return
        department_name = str(self.cbox_Department.currentText())
        department_id = Query().select_Department_by_Name(department_name)[0]
        for row in rows:
            employeeID = int(self.tbl_Employee.item(row, 0).text())
            Query().update_Department_of_Employee(employeeID, department_id)

        self.event_show_messageBox("Application", "Update success")
        self.event_Change_Department()
        self.event_refresh()

    def event_refresh(self):
        self.load_data_table_department(Query().select_All_Department())

    def event_show_messageBox(self, window_title, message_txt):
        mess = QMessageBox()
        mess.setWindowTitle(window_title)
        mess.setText(message_txt)
        if (window_title == "Information"):
            mess.setIcon(QMessageBox.Information)
        else:
            mess.setIcon(QMessageBox.Warning)
        mess.setWindowIcon(QtGui.QIcon("./public/img/back.png"))
        mess.setStandardButtons(QMessageBox.Ok)
        mess.exec_()

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
        text_search = self.txt_Search.text()
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

    def event_create_Department(self):
        department_name = self.txt_DepartmentName.text()
        if (len(department_name) < 1):
            print("Notificatioin: Please Enter Department Name")
            return
        Query().insert_New_Department(department_name)
        self.load_data_table_department(Query().select_All_Department())
