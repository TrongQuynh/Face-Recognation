from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

import sys
import os
import time
from threading import Thread

from Query import Query
from model.Employee import Employee

is_thread_running = False

thread_dataset = None
current_dataset = None


class UI_Employee_List(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/EmployeeList.ui", self)

        self.avatar.setPixmap(QPixmap("./public/img/logoHutech.png"))

        self.employees = None
        self.loadData_table()
        self.format_UI_table()
        self.table_event()
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))

        # self.show()

    def format_UI_table(self):
        # Set select by rows instead of individual cells
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)

        # Set width of
        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 200)
        self.tbl_Employee.setColumnWidth(2, 200)
        self.tbl_Employee.setColumnWidth(3, 250)
        self.tbl_Employee.setColumnWidth(4, 250)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number", "Department"])

    def table_event(self):
        self.tbl_Employee.cellClicked.connect(self.event_cell_was_clicked)

    def loadData_table(self):
        query = Query()
        self.employees = query.select_All_Employee()

        table_row = 0
        # print(self.employees)
        self.tbl_Employee.setRowCount(len(self.employees))
        for e in self.employees:
            department_name = Query().select_Department_by_ID(e[5])[
                1]  # (1, 'IT')
            self.tbl_Employee.setItem(
                table_row, 0, QTableWidgetItem(str(e[0])))
            self.tbl_Employee.setItem(table_row, 1, QTableWidgetItem(e[1]))
            self.tbl_Employee.setItem(table_row, 2, QTableWidgetItem(e[2]))
            self.tbl_Employee.setItem(table_row, 3, QTableWidgetItem(e[3]))
            self.tbl_Employee.setItem(
                table_row, 4, QTableWidgetItem(department_name))
            table_row += 1

    def loadData_to_info_employee(self, employee):
        self.txt_FullName.setText(employee[1])
        self.txt_Gmail.setText(employee[2])
        self.txt_Phonenumber.setText(employee[3])
        department_id = employee[5]
        department_name = Query().select_Department_by_ID(
            department_id)[1]  # (1, 'IT')
        self.txt_Department.setText(department_name)

    def load_dataset(self):
        global is_thread_running
        while (is_thread_running):
            for image in os.listdir(f"./data/dataset/{current_dataset}"):
                # path_str = f"dataset/{name}/{image}"
                path_str = os.path.join(
                    f".\data\dataset\{current_dataset}", image)
                self.dataset_IMG.setPixmap(QPixmap(path_str))
                time.sleep(1)

    def event_load_dataset(self, folder_name):
        global is_thread_running, thread_dataset, current_dataset
        if not os.path.isdir(f"./data/dataset/{folder_name}"):
            print("Notification: Dataset not exist")
            return
        if thread_dataset == None:  # if not have dataset showing
            is_thread_running = True
            current_dataset = folder_name
            thread_dataset = Thread(
                target=self.load_dataset, args=[])
            thread_dataset.start()
        else:
            if (current_dataset == folder_name):
                return
            current_dataset = folder_name
            # thread_dataset = None
            # time.sleep(1)
            # is_thread_running = True
            # thread_dataset = Thread(
            #     target=self.load_dataset, args=(folder_name,))
            # thread_dataset.start()

    def event_cell_was_clicked(self, row, col):
        e_id = self.tbl_Employee.item(row, 0).text()
        employee = Query().select_Employee_by_ID(e_id=e_id)
        folder_name = employee[4]

        self.loadData_to_info_employee(employee)
        self.event_load_dataset(folder_name=folder_name)

    def event_kill_all_thread(self):
        global is_thread_running
        is_thread_running = False
