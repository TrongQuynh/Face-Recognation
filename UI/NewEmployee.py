from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QTableView, QMessageBox
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtCore import QRect, QPropertyAnimation

import time
import os
import shutil
from config.variable import Variable

from Query import Query
from model.Employee import Employee
import cv2


class UI_New_Employee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/NewEmployee.ui", self)
        self.init_table()
        self.employees = []
        self.setWindowFlag(Qt.FramelessWindowHint)
        # self.avatar.setPixmap(QPixmap("./public/img/default_avatar.png"))
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))

        # self.dataSet_IMG.setPixmap(
        #     QPixmap("./data/dataset/NongTrongQuynh-1668938421/1668938421_2.jpg"))

        self.btn_Complete.clicked.connect(self.event_complete)

        self.isOpenCamera = False
        self.getDataset_thread = GetDataset_Thread()
        self.showDataset_thread = LoadDataset_Thread()

        self.btn_FaceData.clicked.connect(self.create_folder_dataset)
        self.btn_takePhoto.clicked.connect(self.event_take_photo)

        self.btn_temporarySave.clicked.connect(self.event_loadData)

        self.btn_ClearRow.clicked.connect(self.event_clear_row_Table)
        self.btn_ClearAll.clicked.connect(self.event_clear_all_row_Table)
        self.btn_ClearData.clicked.connect(self.event_clearTextField)

        self.tbl_Employee.cellClicked.connect(
            self.event_Fill_Data_To_Component)
        self.tbl_Employee.cellClicked.connect(
            self.event_loadDataset)

    def ImageUpdateSlot(self, Image):
        self.lbl_Capture.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateDataset(self, path_img):
        self.dataSet_IMG.setPixmap(QPixmap(str(path_img)))

        # self.show()
    def init_form(self):
        self.load_cbox_data()
        self.time_string = str(int(time.time()))

        self.init_throughScreenText()

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
        self.anim.setStartValue(QRect(-400, 740, 400, 30))
        self.anim.setEndValue(QRect(1700, 740, 400, 30))
        self.anim.setLoopCount(self.loopCount)
        self.anim.start()

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
            self.getDataset_thread.stop()
            return
        shutil.rmtree(f"./data/dataset/{foldername}")

    def validate_dataInput(self):
        fullname = self.txt_Username.text()
        email = self.txt_Email.text()
        phonenumber = self.txt_Phonenumber.text()
        if (self.cbox_Department.currentIndex() == 0):
            self.event_show_messageBox(
                "Warning validate!", "Notification: Please choose department")
            print("Notification: Please choose department")
            return False
        if (fullname == "" or email == "" or phonenumber == ""):
            self.event_show_messageBox(
                "Warning validate!", "Notification: Please enter enough information")
            print("Notification: Please enter enough information")
            return False
        return True

    def init_table(self):
        # Remove index column of table
        self.tbl_Employee.verticalHeader().setVisible(False)
        # Set select by rows instead of individual cells
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Employee.setRowCount(0)

        self.tbl_Employee.setColumnWidth(0, 100)
        self.tbl_Employee.setColumnWidth(0, 200)
        self.tbl_Employee.setColumnWidth(0, 200)
        self.tbl_Employee.setColumnWidth(0, 210)
        self.tbl_Employee.setColumnWidth(0, 210)

        self.tbl_Employee.setHorizontalHeaderLabels(
            ["Full Name", "Email", "Phone Number", "Department", "Folder Name"])

    def create_folder_dataset(self):

        current_row = self.tbl_Employee.currentRow()
        if (current_row < 0):
            self.event_show_messageBox(
                "Warning", "You still not chosen employee")
            print("Notification: Please choose employee")
            return
        folder_name = self.tbl_Employee.item(current_row, 4).text()
        if (self.isOpenCamera):
            self.isOpenCamera = False
            self.getDataset_thread.stop()
            self.event_loadDataset()
            # event show dataset
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

    def clear_TextField(self):
        self.setData(Employee("", "", "", "", 0))

    # Event
    def event_clear_row_Table(self):
        current_row = self.tbl_Employee.currentRow()
        if (current_row < 0):
            self.event_show_messageBox("Warning", "Please choose row")
            print("Notification: Please choose row")
            return

        reply = self.event_show_message_confirm(
            "Warning", "Are you sure wanna delete this row?")
        if (reply == False):
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

    # before excute complete event check if have enough dataset
    def is_enough_dataset(self):
        for e in self.employees:
            dataset = e.dataset
            if not os.path.isdir(f"./data/dataset/{dataset}"):
                return dataset
        return None

    def event_clear_all_row_Table(self):
        # clear all employee in list
        self.employees.clear()
        total_row = self.tbl_Employee.rowCount()
        if (len(self.employees) == 0):
            self.event_show_messageBox(
                "Information", "You do not have any data!")
            return

        reply = self.event_show_message_confirm(
            "Warning", "Are you sure wana delete all row data ?")
        if (reply == False):
            return

        for r in range(total_row):
            folder_name = self.tbl_Employee.item(r, 4).text()
            self.delete_dataset(folder_name)

        self.tbl_Employee.setRowCount(0)
        self.tbl_Employee.clearContents()

    def event_complete(self):
        if (len(self.employees) < 1):
            self.event_show_messageBox(
                "Information", "You do not have any data row!")
            return

        if (dataset := self.is_enough_dataset()):
            reply = self.event_show_message_confirm(
                "Warning", f"Employ is have dataset {dataset} still not have dataset! Are you sure wana complete?")
            if (not reply):
                return

        for e in self.employees:
            Query().insert_Employee(e)

        self.employees.clear()
        self.tbl_Employee.setRowCount(0)
        self.tbl_Employee.clearContents()

        self.event_show_messageBox(
            "Information", f"Insert successful {len(self.employees)} employess")

    def event_loadDataset(self):
        try:
            current_row = self.tbl_Employee.currentRow()
            folder_name = self.tbl_Employee.item(current_row, 4).text()
            print("Current_Row: " + str(current_row))
            self.showDataset_thread.stop()

            self.showDataset_thread.start()
            self.showDataset_thread.folder_name = folder_name

            self.showDataset_thread.ImageUpdate.connect(
                self.ImageUpdateDataset)
        except:
            print("Notitfication: ERORR when load dataset")

    # Load data for table employee
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
        self.clear_TextField()

    def event_clearTextField(self):
        reply = self.event_show_message_confirm(
            "Warning", "Are you sure want to clear all data in text field?")
        if (reply):
            self.clear_TextField()

    def event_take_photo(self):
        if (self.isOpenCamera == False):
            print("Notification: Please Turn ON the camara")
            self.event_show_messageBox("Waring", "You must TURN ON camera!")
            return
        self.getDataset_thread.getDataSet()

    def event_Fill_Data_To_Component(self, row, col):
        fullname = self.tbl_Employee.item(row, 0).text()
        email = self.tbl_Employee.item(row, 1).text()
        phonenumber = self.tbl_Employee.item(row, 2).text()
        department_name = self.tbl_Employee.item(row, 3).text()
        department_ID = self.get_index_department_in_Cbox(department_name)
        print(fullname, email, phonenumber, department_name, department_ID)

        self.setData(Employee(fullname, email,
                     phonenumber, "", int(department_ID)))

    def event_stop_all_thread(self):
        self.getDataset_thread.stop()
        self.showDataset_thread.stop()
        self.loopCount = 0

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

    def event_show_message_confirm(self, window_title, message_txt):
        reply = QMessageBox.question(
            self, window_title, message_txt, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False


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

            centerH = frame.shape[0] // 2
            centerW = frame.shape[1] // 2
            sizeboxW = 300
            sizeboxH = 400
            cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                          (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

            frame = cv2.flip(frame, 1)
            cv2.putText(frame, f"Number: {self.count}", (50, 50),
                        cv2.FONT_HERSHEY_TRIPLEX, 1, (52, 58, 235), 1)

            if self.count < 10 and len(new_frame) > 0:
                self.img_data = new_frame
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = Image
                ConvertToQtFormat = QImage(
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(800, 570, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False

    # Save image into folder
    def getDataSet(self):
        if self.count < 10 and len(self.img_data) > 0:
            if not os.path.isdir(f"./data/dataset/{self.folder_name}"):
                os.mkdir(f"./data/dataset/{self.folder_name}")
            cv2.imwrite(
                f"./data/dataset/{self.folder_name}/{self.user_ID}_{self.count}.jpg", self.img_data)
            print("Save pic: " + str(self.count))
            self.count += 1


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
                # path_str = f"dataset/{name}/{image}"
                path_str = os.path.join(
                    f".\data\dataset\{self.folder_name}", image)
                time.sleep(0.5)
                print(self.folder_name)
                self.ImageUpdate.emit(path_str)
                # self.dataSet_IMG.setPixmap(QPixmap(path_str))

    def stop(self):
        self.ThreadActive = False

    def isThreadRunning(self):
        return self.ThreadActive
