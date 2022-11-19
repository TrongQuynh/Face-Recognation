from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import sys

from Query import Query


class Run_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/EmployeeList.ui", self)

        self.avatar.setPixmap(QPixmap("./public/img/default_avatar.png"))
        self.format_UI_table()
        self.show()
        self.employees = self.loadData()

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

    def loadData(self):
        query = Query()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = Run_UI()

    app.exec_()
