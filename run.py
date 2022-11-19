from PyQt5.QtWidgets import QAction, QApplication, QMessageBox, QWidget
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap

import sys
import time
import os
import shutil
from threading import Thread, Timer

import getDataset
from Query import Query
from model.Employee import Employee

from UI.EmployeeList import UI_Employee_List
from UI.NewEmployee import UI_New_Employee
from UI.Login import Login


class Run_UI():
    def __init__(self):
        self.employeeList = UI_Employee_List()
        # self.employeeList.show()

        self.newEmployee = UI_New_Employee()
        # self.newEmployee.show()

        self.login = Login()
        self.login.btn_Login.clicked.connect(self.event_Login)
        self.login.show()

    def event_Login(self):
        if (self.login.check_Login()):
            print("Login success")
            self.login.hide()
            # self.newEmployee.show()
            self.employeeList.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = Run_UI()

    sys.exit(app.exec_())
