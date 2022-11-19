from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import sys
import os
import time
from threading import Thread

from Query import Query
from model.Employee import Employee


class UI_Employee_List(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Department.ui", self)
        self.departments = None
        self.employees = None

    def intit_table(self):
        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 200)
        self.tbl_Employee.setColumnWidth(2, 200)
        self.tbl_Employee.setColumnWidth(3, 250)
        self.tbl_Employee.setColumnWidth(4, 250)
        self.tbl_Employee.setColumnWidth(5, 250)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number", "Department", "Status"])

        self.tbl_Department.setColumnWidth(0, 50)
        self.tbl_Department.setColumnWidth(1, 200)
        self.tbl_Department.setColumnWidth(2, 200)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number", "Department", "Status"])

    def load_data_table_department(self):
        self.departments = Query().select_All_Department()
        pass

    def load_data_table_employee(self):
        pass
