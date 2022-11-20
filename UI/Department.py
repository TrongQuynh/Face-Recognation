from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import sys
import os
import time
from threading import Thread
from Query import Query


class Department(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Department.ui", self)
        self.center()
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.intit_table()

        self.departments = None
        self.employees = None

        self.load_data_table_department()

        self.tbl_Department.cellClicked.connect(self.event_choose_department)
        self.btn_Search.mousePressEvent = self.event_search_employee

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def intit_table(self):
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
        self.tbl_Department.setColumnWidth(0, 50)
        self.tbl_Department.setColumnWidth(1, 300)
        self.tbl_Department.setColumnWidth(2, 100)
        self.tbl_Department.setHorizontalHeaderLabels(
            ["ID", "Department name", "Total"])

    def load_data_table_department(self):
        self.departments = Query().select_All_Department()
        self.tbl_Department.setRowCount(len(self.departments))
        table_row = 0
        for d in self.departments:
            total_employee = len(
                Query().select_Employee_by_department_ID(int(d[0])))
            self.tbl_Department.setItem(
                table_row, 0, QTableWidgetItem(str(d[0])))
            self.tbl_Department.setItem(table_row, 1, QTableWidgetItem(d[1]))
            self.tbl_Department.setItem(
                table_row, 2, QTableWidgetItem(str(total_employee)))

            table_row += 1
        pass

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
