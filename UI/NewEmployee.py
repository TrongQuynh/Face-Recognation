from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

import sys
import time
import os
import shutil
from threading import Thread, Timer

import getDataset
from Query import Query
from model.Employee import Employee


class UI_New_Employee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/NewEmployee.ui", self)
        self.format_UI_table()
        self.employees = []
        self.avatar.setPixmap(QPixmap("./public/img/default_avatar.png"))
        self.time_string = str(int(time.time()))
        self.load_cbox_data()

        self.btn_Complete.clicked.connect(self.event_complete)
        self.btn_FaceData.clicked.connect(self.create_folder_dataset)
        self.btn_temporarySave.clicked.connect(self.event_loadData)

        self.btn_ClearRow.clicked.connect(self.event_clear_row_Table)
        self.btn_ClearAll.clicked.connect(self.event_clear_all_row_Table)
        self.btn_ClearData.clicked.connect(self.event_clearTextField)

        self.tbl_Employee.cellClicked.connect(self.event_fillData)
        # self.show()

    def getData(self):
        if (not self.validate_dataInput()):
            return None
        fullname = self.txt_Username.text()
        email = self.txt_Email.text()
        phonenumber = self.txt_Phonenumber.text()
        department_name = str(self.cbox_Department.currentText())
        department_id = Query().select_Department_by_Name(department_name)[0]
        dataset = fullname.replace(" ", "") + "-" + str(int(time.time()))

        print(fullname, email, phonenumber, department_id, dataset)
        return Employee(fullname, email, phonenumber, dataset, int(department_id))

    def setData(self, employee):
        self.txt_Username.setText(employee.fullname)
        self.txt_Email.setText(employee.email)
        self.txt_Phonenumber.setText(employee.phonenumber)
        self.cbox_Department.setCurrentIndex(employee.department_id)

    def delete_dataset(self, foldername):
        if not os.path.isdir(f"./data/dataset/{foldername}"):
            print("Notification: Dataset not exist")
            return
        shutil.rmtree(f"./data/dataset/{foldername}")

    def validate_dataInput(self):
        fullname = self.txt_Username.text()
        email = self.txt_Email.text()
        phonenumber = self.txt_Phonenumber.text()
        if (self.cbox_Department.currentIndex() == 0):
            print("Notification: Please choose department")
            return False
        if (fullname == "" or email == "" or phonenumber == ""):
            print("Notification: Please enter enough information")
            return False
        return True

    def format_UI_table(self):
        # Set select by rows instead of individual cells
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Employee.setRowCount(0)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["Full Name", "Email", "Phone Number", "Department", "Folder Name"])

    def create_folder_dataset(self):
        current_row = self.tbl_Employee.currentRow()
        if (current_row < 0):
            print("Notification: Please choose employee")
            return
        folder_name = self.tbl_Employee.item(current_row, 4).text()

        if os.path.isdir(f"./data/dataset/{folder_name}"):
            print("Notification: Dataset already exist")
            return

        getDataset.get_data(folder_name)
        # show dataset
        thread = Thread(target=self.event_loadDataset,
                        args=[folder_name])
        thread.start()

    def get_index_department_in_Cbox(self, department_name):
        for i in range(self.cbox_Department.count()):
            if (self.cbox_Department.itemText(i) == department_name):
                return i
        return -1

    def get_Department_by_name(self, department_name):
        return Query().select_Department_by_Name(department_name)

    def load_cbox_data(self):
        # delete items of list
        self.cbox_Department.clear()

        # [(1, 'IT'), (2, 'Marketing')]
        departments = Query().select_All_Department()
        self.cbox_Department.addItem("None")
        for d in departments:
            self.cbox_Department.addItem(d[1])
    # Event

    def event_clear_row_Table(self):
        current_row = self.tbl_Employee.currentRow()
        if (current_row < 0):
            print("Notification: Please choose row")
            return
        folder_name = self.tbl_Employee.item(current_row, 4).text()
        self.employee = None
        self.tbl_Employee.removeRow(current_row)

        total_row = self.tbl_Employee.rowCount()
        self.tbl_Employee.setRowCount(total_row)
        self.delete_dataset(folder_name)

        # Remove employee from list
        self.employees.pop(current_row)
        # self.tbl_Employee.clearContents()

    def event_clear_all_row_Table(self):
        # clear all employee in list
        self.employees.clear()
        total_row = self.tbl_Employee.rowCount()
        for r in range(total_row):
            folder_name = self.tbl_Employee.item(r, 4).text()
            self.delete_dataset(folder_name)

        self.tbl_Employee.setRowCount(0)
        self.tbl_Employee.clearContents()

    def event_complete(self):
        if (len(self.employees) < 1):
            return
        for e in self.employees:
            Query().insert_Employee(e)

    def event_loadDataset(self, folderName):
        if not os.path.isdir(f"./data/dataset/{folderName}"):
            print("Notification: Not found folder")
            return

        for image in os.listdir(f"./data/dataset/{folderName}"):
            # path_str = f"dataset/{name}/{image}"
            path_str = os.path.join(f".\data\dataset\{folderName}", image)
            time.sleep(0.5)
            self.dataSet_IMG.setPixmap(QPixmap(path_str))
            # self.showDataSet(path_str)
        Timer(1, self.event_loadDataset, args=[folderName])

    def event_loadData(self):
        employee = self.getData()

        table_row = self.tbl_Employee.rowCount()
        if (not employee):
            return
        self.employees.append(employee)
        self.tbl_Employee.setRowCount(table_row + 1)

        self.tbl_Employee.setItem(
            table_row, 0, QTableWidgetItem(employee.fullname))
        self.tbl_Employee.setItem(
            table_row, 1, QTableWidgetItem(employee.email))
        self.tbl_Employee.setItem(
            table_row, 2, QTableWidgetItem(employee.phonenumber))
        self.tbl_Employee.setItem(table_row, 3, QTableWidgetItem(
            str(self.cbox_Department.currentText())))
        self.tbl_Employee.setItem(
            table_row, 4, QTableWidgetItem(employee.dataset))

        # Clear Text field
        self.event_clearTextField()

    def event_clearTextField(self):
        self.setData(Employee("", "", "", "", 0))

    def temporary_save(self): pass

    def event_fillData(self, row, col):
        fullname = self.tbl_Employee.item(row, 0).text()
        email = self.tbl_Employee.item(row, 1).text()
        phonenumber = self.tbl_Employee.item(row, 2).text()
        department_name = self.tbl_Employee.item(row, 3).text()
        department_ID = self.get_index_department_in_Cbox(department_name)
        print(fullname, email, phonenumber, department_name, department_ID)

        self.setData(Employee(fullname, email,
                     phonenumber, "", int(department_ID)))
