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


class UI_Edit_Employee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/EditEmployee.ui", self)
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

        self.btn_Back.mousePressEvent = self.event_click_back
        self.lbl_Close.mousePressEvent = self.event_close_app

        self.btn_FaceData.clicked.connect(self.create_folder_dataset)
        self.btn_takePhoto.clicked.connect(self.event_take_photo)

        self.btn_ClearData.clicked.connect(self.event_clearTextField)

    def ImageUpdateSlot(self, Image):
        self.lbl_Capture.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateDataset(self, path_img):
        self.dataSet_IMG.setPixmap(QPixmap(str(path_img)))

        # self.show()
    def init_form(self):
        self.load_cbox_data()
        self.time_string = str(int(time.time()))
        self.showDataset_thread = LoadDataset_Thread()
        self.init_throughScreenText()

    def init_throughScreenText(self):
        self.label_Text.setText("HUTECH INSTITUTE of INTERNATIONAL EDUCATION")
        self.setStyleSheet("#label_Text{color : yellow}")
        self.label_Text.move(-30, 680)
        self.loopCount = 100
        self.doAnim()

    def load_cbox_data(self):
        # delete items of list
        self.cbox_Department.clear()

        # [(1, 'IT'), (2, 'Marketing')]
        departments = Query().select_All_Department()
        self.cbox_Department.addItem("None")
        for d in departments:
            self.cbox_Department.addItem(d[1])

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
        dataset = self.employee.dataset

        employee = Employee(fullname, email, phonenumber,
                            dataset, int(department_id))
        employee.id = self.employee.id
        self.employee = employee
        return employee

    def setData(self, employee):
        self.employee = employee
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

    def create_folder_dataset(self):

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

    def event_load_dataset(self, folder_name):

        if not os.path.isdir(f"./data/dataset/{folder_name}"):
            print("Notification: Dataset not exist")
            return
        self.showDataset_thread.start()
        self.showDataset_thread.folder_name = folder_name
        self.showDataset_thread.ImageUpdate.connect(self.ImageUpdateDataset)

    def is_enough_dataset(self):
        if not os.path.isdir(f"./data/dataset/{self.employee.dataset}"):
            return self.employee.fullname
        return None

    def event_complete(self):
        reply = self.event_show_message_confirm(
            "Warning", "Are you sure wanna complete ?")
        if (fullname := self.is_enough_dataset()):
            reply = self.event_show_message_confirm(
                "Warning", f"Employ with name {fullname} still not have dataset! Are you sure wana complete?")
            if (not reply):
                return

        if (self.employee.fullname != str(self.txt_Username.text())):
            new_name_data_set = str(self.txt_Username.text()).replace(
                " ", "") + "-" + str(int(time.time()))
            # replace folder name
            os.rename(f"./data/dataset/{self.employee.dataset}",
                      f"./data/dataset/{new_name_data_set}")
            self.employee.dataset = new_name_data_set

        self.getData()
        Query().update_Employee_by_ID(self.employee, self.employee.id)

        self.event_show_messageBox(
            "Information", f"Update successful 1 employess")
        self.event_back()

    def set_UI_employee_list(self, UI):
        self.UI_Employee = UI

    def event_click_back(self, *arg, **kwargs):
        self.event_back()

    def event_back(self):
        self.hide()
        self.UI_Employee.show()
        self.UI_Employee.load_all_employee_into_table()
        self.event_stop_all_thread()

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

    def event_close_app(self, *arg, **kwargs):
        reply = self.event_show_message_confirm(
            "Application", "Are you sure wanna close app ?")
        if (reply):
            self.close()

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

            if self.count < 5 and len(new_frame) > 0:
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
        if self.count < 5 and len(self.img_data) > 0:
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
