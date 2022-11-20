from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import sys
import os
import time
from threading import Thread

from Query import Query
from model.Employee import Employee
from UI.NewEmployee import UI_New_Employee
from UI.EmployeeList import UI_Employee_List
from UI.Department import Department


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Home.ui", self)

        self.UI_addEmployee = UI_New_Employee()
        self.UI_employeeList = UI_Employee_List()
        self.UI_department = Department()

        self.lbl_background.setPixmap(
            QPixmap("./public/img/employee-background.jfif"))

        self.pushButton_8.clicked.connect(
            lambda: self.event_change_form("newEmployee"))
        self.pushButton_11.clicked.connect(
            lambda: self.event_change_form("employee"))
        self.pushButton_14.clicked.connect(
            lambda: self.event_change_form("department"))
        self.UI_employeeList.btn_Back.mousePressEvent = self.event_back_to_home
        self.UI_addEmployee.btn_Back.mousePressEvent = self.event_back_to_home

    def event_change_form(self, form):
        if (form == "newEmployee"):
            self.UI_addEmployee.show()
            self.hide()
        elif (form == "employee"):
            self.UI_employeeList.show()
            self.hide()
        elif (form == "department"):
            self.UI_department.show()
            self.hide()

    def event_back_to_home(self, *arg, **kwargs):
        self.show()
        self.UI_employeeList.hide()
