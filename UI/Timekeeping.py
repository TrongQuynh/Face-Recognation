from threading import Thread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtCore import QRect, QPropertyAnimation

import cv2
import os
import time
from Query import Query
from config.variable import Variable
from datetime import datetime, date

from model.Time_KP_Recoed import TimekeepingRecord


class Timekeeping(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Timekeeping.ui", self)
        self.center()
        self.employees = []
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))
        self.logo.setPixmap(
            QPixmap("./public/img/logoHutech.png"))

        self.save_TK_thread_isRunning = False

        # self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))

    def init_form(self):

        self.lbl_Date.setText(str((date.today()).strftime("%d/%m/%Y")))
        self.init_table()
        self.load_data_to_TK_table()

        self.recognize_thread = Recognize_thread()
        self.recognize_thread.start()
        self.recognize_thread.ImageUpdate.connect(self.ImageUpdateSlot)
        self.recognize_thread.AddTimekeeping.connect(self.add_timekeeping)
        self.recognize_thread.UpdateCurrentTime.connect(
            self.event_show_current_time)

        self.init_throughScreenText()
        self.TE_TimeOut.setTime(QTime(17, 0, 0))

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
        self.lbl_Timekeeping.verticalHeader().setVisible(False)

        self.lbl_Timekeeping.setSelectionBehavior(QTableView.SelectRows)

        self.lbl_Timekeeping.setColumnWidth(0, 50)
        self.lbl_Timekeeping.setColumnWidth(1, 200)
        self.lbl_Timekeeping.setColumnWidth(2, 95)
        self.lbl_Timekeeping.setColumnWidth(3, 150)
        self.lbl_Timekeeping.setColumnWidth(4, 150)
        self.lbl_Timekeeping.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Department", "Time In", "Time Out"])

    def load_data_to_TK_table(self):
        date_today = date.today()
        TK_Record = Query().select_All_TKRecord_by_Date(date_today)
        # table_row = self.tbl_Employee.rowCount()
        self.lbl_Timekeeping.setRowCount(len(TK_Record))
        table_row = 0
        for record in TK_Record:
            employee = Query().select_Employee_by_ID(int(record[4]))
            #(19, 'Nong Trong Quynh', 'abc@gmail.com', '093866522341', 'NongTrongQuynh-1669052513', 1)
            department_name = Query().select_Department_by_ID(
                int(employee[5]))[1]
            self.lbl_Timekeeping.setItem(
                table_row, 0, QTableWidgetItem(str(employee[0])))
            self.lbl_Timekeeping.setItem(
                table_row, 1, QTableWidgetItem(employee[1]))
            self.lbl_Timekeeping.setItem(
                table_row, 2, QTableWidgetItem(department_name))
            self.lbl_Timekeeping.setItem(
                table_row, 3, QTableWidgetItem(str(record[2])))
            self.lbl_Timekeeping.setItem(
                table_row, 4, QTableWidgetItem(str(record[3])))
            table_row += 1

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def event_stop_all_thread(self):
        self.recognize_thread.stop()
        self.loopCount = 0
        # self.clock_thread.stop()

    def ImageUpdateSlot(self, Image):
        self.lbl_Capture.setPixmap(QPixmap.fromImage(Image))

    def isEmployeeHaveTimekeeping_TimeIn(self, employee_ID):
        # return true if employee have time in
        date_today = date.today()
        timekeeping_record_today = Query().select_All_TKRecord_by_Date(date_today)
        for record in timekeeping_record_today:
            if (int(record[4]) == int(employee_ID) and record[2]):
                return True
        return False

    def is_Time1_Larger_Than_Time2(self, time1, time2):
        t_1 = datetime.strptime(f"{time1}", "%H:%M:%S")
        t_2 = datetime.strptime(f"{time2}", "%H:%M:%S")
        return t_1 >= t_2

    def new_save_TK_thread(self):
        self.save_TK_thread_isRunning = False

    def add_timekeeping(self, dataset):
        if (self.save_TK_thread_isRunning == False):
            self.save_Timekeeping_thread = Save_Timekeeping_thread()

            self.save_Timekeeping_thread.TE_TimeOut = self.TE_TimeOut
            self.save_Timekeeping_thread.dataset = dataset
            self.save_TK_thread_isRunning = True
            self.save_Timekeeping_thread.LoadDataTable.connect(
                self.load_data_to_TK_table)
            self.save_Timekeeping_thread.New_Save_Timekeeping_thread.connect(
                self.new_save_TK_thread)
            self.save_Timekeeping_thread.start()
        # self.load_data_to_employee_table()

    def event_show_current_time(self):
        str_time = time.strftime("%H:%M:%S", time.localtime())
        self.lbl_Clock.setText(str_time)


class Recognize_thread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    AddTimekeeping = pyqtSignal(str)
    UpdateCurrentTime = pyqtSignal()

    face_cascaded = cv2.CascadeClassifier(
        f"{os.getcwd()}\config\haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.isfile(f"./data/tranning/training.yml"):
        print("Not have tranning model")
        recognizer = None
    else:
        recognizer.read(f"{os.getcwd()}\\data\\tranning\\training.yml")

    start_time = 0
    names = {}
    employees = []

    for user in os.listdir("./data/dataset/"):
        id = int(os.listdir(f"./data/dataset/{user}")[0].split('_')[0])
        names[id] = user

    def run(self):
        if (self.recognizer == None):
            return
        self.ThreadActive = True
        Capture = cv2.VideoCapture(Variable().index_Capture)
        while self.ThreadActive:
            ret, frame = Capture.read()

            # Flip Image
            # frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascaded.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                x1 = x
                y1 = y
                x2 = x1 + w
                y2 = y1 + h
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Prefic and get ID user
                id, confidence = self.recognizer.predict(gray[y1:y2, x1:x2])

                username = str(self.names[id]).split("-")[0]
                print(username, confidence)

                # print(username)
                # confidence_format = f"{int(confidence)} %"
                confidence_format = "  {0}%".format(round(100 - confidence))

                if (confidence < 70):

                    if (self.employees.count(id) == 50):
                        self.AddTimekeeping.emit(str(self.names[id]))
                        self.employees.append(id)
                        # print(self.employees)
                        print(f"{username} 50 times")
                        self.employees[:] = (
                            value for value in self.employees if value != id)
                    else:
                        self.employees.append(id)
                else:
                    username = "Unknown"
                    # confidence_format = "---"
                cv2.putText(
                    frame, username, (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
                # cv2.putText(
                #     frame, confidence_format, (x1, y2), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))

            # Show FPS
            current_time = time.time()
            fps = int(1 / (current_time - self.start_time))
            self.start_time = current_time
            cv2.putText(frame, f"FPS: {fps}", (50, 50),
                        cv2.FONT_HERSHEY_TRIPLEX, 1, (52, 58, 235), 1)
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = Image
                ConvertToQtFormat = QImage(
                    FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(800, 590, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                self.UpdateCurrentTime.emit()

    def stop(self):
        self.ThreadActive = False


class Save_Timekeeping_thread(QThread):
    dataset = None
    LoadDataTable = pyqtSignal()
    New_Save_Timekeeping_thread = pyqtSignal()

    def is_Time1_Larger_Than_Time2(self, time1, time2):
        t_1 = datetime.strptime(f"{time1}", "%H:%M:%S")
        t_2 = datetime.strptime(f"{time2}", "%H:%M:%S")
        return t_1 >= t_2

    def run(self):
        employee = Query().select_Employee_by_dataset(self.dataset)
        print(self.TE_TimeOut.time().toString())

        date_today = date.today()
        TR_e_today = Query().select_All_TKRecord_by_EmployeeID_and_Date(
            int(employee[0]), date_today)

        # Check if this employee has timekeeping or not(ckeck in or check in and check out)
        if (TR_e_today):

            # if today employee has check out -> return and restart thread
            e_time_out = TR_e_today[3]
            if (e_time_out != None):
                print(f"{str(employee[1])} has timekeeping today")
                self.New_Save_Timekeeping_thread.emit()
                return

            time_out = self.TE_TimeOut.time().toString()
            current_time = time.strftime("%H:%M:%S", time.localtime())

            # if current time is larger than time out
            if (self.is_Time1_Larger_Than_Time2(current_time, time_out)):
                # update
                TR_id = TR_e_today[0]
                print(int(employee[0]), TR_id)
                Query().update_Timekeeping_Record(
                    int(employee[0]), int(TR_id[0]))
        else:
            # if this employee not have time in
            T_Record = TimekeepingRecord(int(employee[0]))
            Query().insert_Timekeeping_Record(T_Record)

        #
        self.LoadDataTable.emit()
        self.New_Save_Timekeeping_thread.emit()

    def stop(self):
        self.ThreadActive = False


class Clock_Thread(QThread):
    UpdateCurrentTime = pyqtSignal()

    def run(self):
        self.ThreadActivity = True
        # target function of the thread class
        try:
            while self.ThreadActivity:
                self.UpdateCurrentTime.emit()

        finally:
            print("Thread Clock end")

    def stop(self):
        self.ThreadActivity = False

# https: // codetorial.net/en/pyqt5/basics/datetime.html
