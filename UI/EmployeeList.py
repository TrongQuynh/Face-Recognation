from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QTableView
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal
import shutil

from PyQt5.QtCore import QRect, QPropertyAnimation
import os
import time
from threading import Thread

from Query import Query
from model.Employee import Employee

from UI.EditEmployee import UI_Edit_Employee

is_thread_running = False

thread_dataset = None
current_dataset = None


class UI_Employee_List(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/EmployeeList.ui", self)

        self.avatar.setPixmap(QPixmap("./public/img/logoHutech.png"))
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))
        self.employees = None
        self.init_table()
        self.table_event()
        self.btn_Delete.clicked.connect(self.event_delete_employee)
        self.btn_Search.clicked.connect(self.event_search)
        self.btn_Edit.clicked.connect(self.event_edit_employee)
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))

        # self.show()
    def init_form(self):
        self.load_all_employee_into_table()
        self.init_throughScreenText()
        self.showDataset_thread = LoadDataset_Thread()

    def load_all_employee_into_table(self):
        query = Query()
        employees = query.select_All_Employee()
        self.loadData_table(employees)

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

    def init_table(self):
        # Remove index of table
        self.tbl_Employee.verticalHeader().setVisible(False)
        # Set select by rows instead of individual cells
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)

        # Set width of
        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 250)
        self.tbl_Employee.setColumnWidth(2, 265)
        self.tbl_Employee.setColumnWidth(3, 262)
        self.tbl_Employee.setColumnWidth(4, 250)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Email", "Phone Number", "Department"])

    def table_event(self):
        self.tbl_Employee.cellClicked.connect(self.event_cell_was_clicked)

    def loadData_table(self, employees):

        table_row = 0
        self.tbl_Employee.setRowCount(len(employees))
        for e in employees:
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

    def event_load_dataset(self, folder_name):

        if not os.path.isdir(f"./data/dataset/{folder_name}"):
            print("Notification: Dataset not exist")
            return
        self.showDataset_thread.start()
        self.showDataset_thread.folder_name = folder_name
        self.showDataset_thread.ImageUpdate.connect(self.ImageUpdateDataset)

    def ImageUpdateDataset(self, path_img):
        self.dataset_IMG.setPixmap(QPixmap(str(path_img)))

    def event_cell_was_clicked(self, row, col):
        e_id = self.tbl_Employee.item(row, 0).text()
        employee = Query().select_Employee_by_ID(e_id=e_id)
        folder_name = employee[4]

        self.loadData_to_info_employee(employee)
        self.event_load_dataset(folder_name=folder_name)

    def event_stop_all_thread(self):
        self.loopCount = 0
        self.showDataset_thread.stop()

    def event_show_message_confirm(self, winTitle, message):
        mess = QMessageBox()
        mess.setWindowTitle(winTitle)
        mess.setText(message)

        mess.setIcon(QMessageBox.Warning)
        mess.setWindowIcon(QtGui.QIcon("./public/img/back.png"))
        mess.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if mess.exec_() == QMessageBox.Yes:
            return True
        return False

    def event_edit_employee(self):
        current_row = self.tbl_Employee.currentRow()
        print(current_row)
        if (current_row < 0):
            print("Notification: Please choose employee")
            return
        employee_ID = int(self.tbl_Employee.item(current_row, 0).text())
        employee_Data = Query().select_Employee_by_ID(employee_ID)
        self.UI_EditEmployee = UI_Edit_Employee()
        self.UI_EditEmployee.init_form()
        self.UI_EditEmployee.show()
        employee = Employee(employee_Data[1], employee_Data[3],
                            employee_Data[2], employee_Data[4], int(employee_Data[5]))
        employee.id = employee_Data[0]
        self.UI_EditEmployee.setData(employee)
        self.UI_EditEmployee.event_load_dataset(employee_Data[4])
        self.UI_EditEmployee.set_UI_employee_list(self)
        self.hide()

    def event_delete_employee(self):
        current_row = self.tbl_Employee.currentRow()
        if (current_row < 0):
            print("Notification: Please choose employee")
            return
        employee_name = str(self.tbl_Employee.item(current_row, 1).text())
        reply = self.event_show_message_confirm(
            "Warning", f"Are you sure wanna delete employee {employee_name} ?")
        if (reply == False):
            return
        employee_ID = int(self.tbl_Employee.item(current_row, 0).text())
        dataset = Query().select_Employee_by_ID(employee_ID)[4]
        self.delete_dataset(dataset)
        Query().delete_All_TKRecord_by_EmployeeID(employee_ID)
        Query().delete_Employee_by_ID(employee_ID)
        employees = Query().select_All_Employee()
        self.loadData_table(employees)

    # Helper

    def delete_dataset(self, foldername):
        if not os.path.isdir(f"./data/dataset/{foldername}"):
            print("Notification: Dataset not exist")
            self.getDataset_thread.stop()
            return
        shutil.rmtree(f"./data/dataset/{foldername}")

    def is_number(self, number):
        try:
            int(number)
            return True
        except:
            return False

    def event_search(self):
        employees = Query().select_All_Employee()
        employee_list = []
        text_search = self.txt_Search.text()
        if (self.is_number(text_search)):
            for e in employees:
                if e[0] == int(text_search):
                    employee_list.append(e)
            self.loadData_table(employee_list)
        else:
            for e in employees:
                e_FName = str(e[1]).replace(" ", "").lower()
                search_FName = str(text_search).replace(" ", "").lower()
                if search_FName in e_FName or e_FName in search_FName:
                    employee_list.append(e)
            self.loadData_table(employee_list)


class LoadDataset_Thread(QThread):
    folder_name = None
    ImageUpdate = pyqtSignal(str)

    def run(self):
        self.ThreadActive = True
        while (self.ThreadActive):

            if not os.path.isdir(f"./data/dataset/{self.folder_name}"):
                print("Notification: Not found folder: " +
                      str(f"{os.getcwd()}/data/dataset/{self.folder_name}"))
                self.stop()
                return
            for image in os.listdir(f"./data/dataset/{self.folder_name}"):
                path_str = os.path.join(
                    f".\data\dataset\{self.folder_name}", image)
                time.sleep(0.5)
                self.ImageUpdate.emit(path_str)
            print(self.folder_name)

    def stop(self):
        self.ThreadActive = False
