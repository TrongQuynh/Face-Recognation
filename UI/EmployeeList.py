from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QTableView, QFileDialog
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import QThread, Qt, pyqtSignal
import shutil

from PyQt5.QtCore import QRect, QPropertyAnimation
import os
import time
from config.variable import Variable
import cv2

import pandas as pd
import openpyxl

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
        self.employee = None
        self.init_table()
        self.table_event()
        self.btn_Delete.clicked.connect(self.event_delete_employee)
        self.btn_Search.clicked.connect(self.event_search)
        
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.btn_Excel.clicked.connect(self.event_Open_Dialog)
        
        self.isOpenCamera = False
        self.getDataset_thread = GetDataset_Thread()
        self.btn_OpenCamera.clicked.connect(self.create_folder_dataset)
        self.btn_TakePhoto.clicked.connect(self.event_take_photo)
        self.btn_Edit.clicked.connect(self.event_edit_employee)
        
        # self.btn_Dataset.clicked.connect(self.chooseDataset)

        # self.show()
    def init_form(self):
        self.lbl_newDataset.setPixmap(QPixmap())
        self.dataset_IMG.setPixmap(QPixmap())
        
        self.load_all_employee_into_table()
        self.init_throughScreenText()
        self.load_cbox_data()
        
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
        
        self.loadData_to_update_employee(employee)

    def load_cbox_data(self):
        # delete items of list
        self.cbox_Department.clear()

        # [(1, 'IT'), (2, 'Marketing')]
        departments = Query().select_All_Department()
        self.cbox_Department.addItem("None")
        for d in departments:
            self.cbox_Department.addItem(d[1])

    def get_index_department_in_Cbox(self, department_name):
        for i in range(self.cbox_Department.count()):
            if (self.cbox_Department.itemText(i) == department_name):
                return i
        return -1
    
    def loadData_to_update_employee(self,employee):
        self.txt_FullName_2.setText(employee[1])
        self.txt_Email.setText(employee[2])
        self.txt_PhoneNumber.setText(employee[3])
        department_id = employee[5]
        department_name = Query().select_Department_by_ID(
            department_id)[1]
        
        self.cbox_Department.setCurrentIndex(self.get_index_department_in_Cbox(department_name))
    
    def is_have_dataset(self):
        if not os.path.isdir(f"./data/dataset/{self.employee.dataset}"):
            return self.employee.fullname
        return None
    
    def event_update_employee(self):
        
        reply = self.event_show_message_confirm(
            "Warning", "Are you sure wanna complete ?")
        if (fullname := self.is_have_dataset()):
            reply = self.event_show_message_confirm(
                "Warning", f"Employ with name {fullname} still not have dataset! Are you sure wana complete?")
            if (not reply):
                return
        
        if (self.employee.fullname != str(self.txt_FullName_2.text())):
            new_name_data_set = str(self.txt_FullName_2.text()).replace(
                " ", "") + "-" + str(int(time.time()))
            # replace folder name
            os.rename(f"./data/dataset/{self.employee.dataset}",
                      f"./data/dataset/{new_name_data_set}")
            self.employee.dataset = new_name_data_set
        
        fullname = self.txt_FullName_2.text()
        email = self.txt_Email.text()
        phonenumber = self.txt_PhoneNumber.text()
        department_name = str(self.cbox_Department.currentText())
        department_id = Query().select_Department_by_Name(department_name)[0]
        dataset = self.employee.dataset
        # if(dataset != self.TMP_DatasetFolder):
        #     dataset = self.TMP_DatasetFolder
        #     self.employee.dataset = self.TMP_DatasetFolder
        #     os.rename(f"./data/dataset/{self.employee.dataset}",
        #               f"./data/dataset/{new_name_data_set}")
        
        employee = Employee(fullname, email, phonenumber,
                            dataset, int(department_id))
        employee.id = self.employee.id
        Query().update_Employee_by_ID(employee, employee.id)
        self.employee = employee
        self.event_show_messageBox("Mesage","Update success!")

    def ImageUpdateSlot(self, Image):
        self.lbl_newDataset.setPixmap(QPixmap.fromImage(Image))
    
    def create_folder_dataset(self):
        if(self.employee == None):
            self.event_show_messageBox("Message","Please choose employee!")
            return
        folder_name = self.employee.dataset
        if (self.isOpenCamera):
            self.isOpenCamera = False
            self.getDataset_thread.stop()
            # event show dataset
            self.event_load_dataset(folder_name)
            return
        if os.path.isdir(f"./data/dataset/{folder_name}"):
            reply = self.event_show_message_confirm(
                "Warning", "Dataset already exist do you want replace it ?")
            if (reply == False):
                print("Notification: Dataset already exist")
                return
            else:
                self.delete_dataset(folder_name)

        if (self.isOpenCamera == False):
            self.getDataset_thread.folder_name = folder_name
            self.getDataset_thread.start()
            self.getDataset_thread.ImageUpdate.connect(self.ImageUpdateSlot)
            self.isOpenCamera = True
            
    def event_take_photo(self):
        if (self.isOpenCamera == False):
            print("Notification: Please Turn ON the camara")
            self.event_show_messageBox("Waring", "You must TURN ON camera!")
            return
        self.getDataset_thread.getDataSet()
    
    def event_show_messageBox(self, window_title, message_txt):
        mess = QMessageBox()
        mess.setWindowTitle(window_title)
        mess.setText(message_txt)
        if (window_title == "Information"):
            mess.setIcon(QMessageBox.Information)
        else:
            mess.setIcon(QMessageBox.Warning)
        mess.setWindowIcon(QtGui.QIcon("./public/img/back.png"))
        mess.setStandardButtons(QMessageBox.Ok)
        mess.exec_()
    
    def event_load_dataset(self, folder_name):

        if not os.path.isdir(f"./data/dataset/{folder_name}"):
            print("Notification: Dataset not exist")
            return
        self.showDataset_thread.stop()
        self.showDataset_thread.start()
        self.showDataset_thread.folder_name = folder_name
        self.showDataset_thread.ImageUpdate.connect(self.ImageUpdateDataset)

    def event_Open_Dialog(self):
        reply = self.event_show_message_confirm(
            "Export Excel", "Do you wanna export excel?")
        if (reply == False):
            return
        file = QFileDialog.getSaveFileName()
        path = f"{file[0]}.xlsx"

        fileName = f'./data/excel/{path.split("/")[-1]}'
        sheetname = 'Employee_List'

        employees = []
        for employee in Query().select_All_Employee():
            department_name = Query().select_Department_by_ID(employee[5])[1]
            employees.append(
                [employee[0], employee[1], employee[3], employee[2], department_name])
        print(employees)
        df = pd.DataFrame(employees,
                          columns=["Employee ID", "Full Name", "Email", "Phonenumber", "Department"])
        df.to_excel(fileName,
                    sheet_name=sheetname, index=False, startrow=0, startcol=0)

    def chooseDataset(self):
        if(self.employee == None):
            return
        # file = QFileDialog.getExistingDirectory()
        # r_file = (file.split("/"))[-1]
        # self.TMP_DatasetFolder = r_file
        # self.txt_NewDatasetName.setText(r_file)
        # print(r_file)
    
    def ImageUpdateDataset(self, path_img):
        self.dataset_IMG.setPixmap(QPixmap(str(path_img)))

    def event_cell_was_clicked(self, row, col):
        e_id = self.tbl_Employee.item(row, 0).text()
        employee = Query().select_Employee_by_ID(e_id=e_id)
        folder_name = employee[4]

        self.employee = Employee(employee[1], employee[3],
                            employee[2], employee[4], int(employee[5]))
        self.TMP_DatasetFolder = employee[4]
        self.employee.id = employee[0]
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
        self.event_update_employee()
        self.load_all_employee_into_table()
 
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
            self.showDataset_thread.stop()
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
                if(self.ThreadActive == False):
                    break
                path_str = os.path.join(
                    f".\data\dataset\{self.folder_name}", image)
                time.sleep(0.5)
                self.ImageUpdate.emit(path_str)
            print(self.folder_name)

    def stop(self):
        self.ThreadActive = False


class GetDataset_Thread(QThread):
    face_cascaded = cv2.CascadeClassifier(
        "./config/haarcascade_frontalface_default.xml")
    folder_name = None
    ImageUpdate = pyqtSignal(QImage)
    img_data = None

    def run(self):
        self.ThreadActive = True
        print("Folder name: " + str(self.folder_name))
        self.count = 0
        arr = str(self.folder_name).split("-")
        self.user_ID = str(arr[1])
        capture = cv2.VideoCapture(Variable().index_Capture)
        while self.ThreadActive:
            ret, frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascaded.detectMultiScale(gray, 1.3, 5)
            new_frame = []
            for (x, y, W, h) in faces:
                x1 = x
                y1 = y
                x2 = x1 + W
                y2 = y1 + h
                cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(
                    x2, y2), color=(0, 255, 0), thickness=4)

                # frame[:W, :h] = frame[y1:y2, x1:x2]
                new_frame = gray[y1:y2, x1:x2].copy()

            frame = cv2.flip(frame, 1)
            cv2.putText(frame, f"Number: {self.count}", (50, 50),
                        cv2.FONT_HERSHEY_TRIPLEX, 1, (52, 58, 235), 1)

            if self.count < 5 and len(new_frame) > 0:
                self.img_data = new_frame
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = Image
                ConvertToQtFormat = QImage(
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(400, 470, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False

    # Save image into folder
    def getDataSet(self):
        if self.count < 5 and len(self.img_data) > 0:
            if not os.path.isdir(f"./data/dataset/{self.folder_name}"):
                os.mkdir(f"./data/dataset/{self.folder_name}")
            cv2.imwrite(
                f"./data/dataset/{self.folder_name}/{self.user_ID}_{self.count}.jpg", self.img_data)
            print("Save pic: " + str(self.count))
            self.count += 1