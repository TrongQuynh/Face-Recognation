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
from UI.Home import Home
from UI.Login import Login
# from UI.Department import Department
from UI.TimekeepingRecord import Timekeeping_Record
from UI.Timekeeping import Timekeeping


class Run_UI():
    def __init__(self):

        # self.department_UI = Department()
        # self.timekeepingRecord_UI = Timekeeping_Record()
        # self.timekeeping_UI = Timekeeping()
        self.home = Home()

        self.login = Login()
        self.login.btn_Login.clicked.connect(self.event_Login)
        self.login.show()

    def event_Login(self):
        if (self.login.check_Login()):
            print("Login success")
            self.login.hide()

            self.home.show()
            # self.department_UI.show()
            # self.timekeepingRecord_UI.show()
            # self.timekeeping_UI.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = Run_UI()

    sys.exit(app.exec_())
