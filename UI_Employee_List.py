from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import sys

from Query import Query
from model.Employee import Employee


class UI_Employee_List(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/EmployeeList.ui", self)

        self.avatar.setPixmap(QPixmap("./public/img/default_avatar.png"))

        self.employees = self.loadData()
        self.format_UI_table()
        self.table_event()
        self.show()

    def format_UI_table(self):
        # Set select by rows instead of individual cells
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)

        # Set width of
        self.tbl_Employee.setColumnWidth(0, 80)
        self.tbl_Employee.setColumnWidth(3, 150)
        self.tbl_Employee.setColumnWidth(4, 150)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number", "Department"])
        # self.tbl_Employee.

    def table_event(self):
        self.tbl_Employee.cellClicked.connect(self.cell_was_clicked)

    def cell_was_clicked(self, row, col):
        e_id = self.tbl_Employee.item(row, 0).text()
        employee = Query().select_Employee_by_ID(e_id=e_id)
        self.loadData_to_info_employee(employee)

    def loadData(self):
        query = Employee
        self.employees = query.select_All_Employee()
        self.tbl_Employee.setRowCount(50)
        table_row = 0
        # print(self.employees)
        for e in self.employees:

            self.tbl_Employee.setItem(
                table_row, 0, QTableWidgetItem(str(e[0])))
            self.tbl_Employee.setItem(table_row, 1, QTableWidgetItem(e[1]))
            self.tbl_Employee.setItem(table_row, 2, QTableWidgetItem(e[2]))
            self.tbl_Employee.setItem(table_row, 3, QTableWidgetItem(e[3]))
            self.tbl_Employee.setItem(table_row, 4, QTableWidgetItem(e[4]))
            table_row += 1

    def loadData_to_info_employee(self, employee):
        self.txt_FullName.setText(employee[1])
        self.txt_Gmail.setText(employee[2])
        self.txt_Phonenumber.setText(employee[3])
        self.txt_Department.setText("IT")
