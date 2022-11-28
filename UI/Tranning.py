from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidgetItem, QTableView, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtCore import QRect, QPropertyAnimation

from PIL import Image
import os
import time
import cv2
import numpy as np
from Query import Query


class Tranning(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Tranning.ui", self)
        self.center()
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))
        # self.dataset_IMG.setPixmap(
        #     QPixmap("./data/dataset/ThienAn-1668564194/1668564194_47.jpg"))

        self.intit_table()
        self.tbl_Employee.cellClicked.connect(
            self.event_table_employee_was_clicked)
        self.btn_Tranning.clicked.connect(self.event_tranning_data)
        self.employees = None

    def init_form(self):
        self.load_data_table_employee()

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
        self.anim.setStartValue(QRect(-400, 730, 400, 30))
        self.anim.setEndValue(QRect(1700, 730, 400, 30))
        self.anim.setLoopCount(self.loopCount)
        self.anim.start()

    def ImageUpdateDataset(self, path_img):
        self.dataset_IMG.setPixmap(QPixmap(str(path_img)))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def intit_table(self):
        self.tbl_Employee.verticalHeader().setVisible(False)
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)

        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 200)
        self.tbl_Employee.setColumnWidth(2, 200)
        self.tbl_Employee.setColumnWidth(3, 200)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Department", "Dataset"])

    def load_data_table_employee(self):
        self.employees = Query().select_All_Employee()
        if (len(self.employees) < 1):
            print("Notification: Not found employee")
        self.tbl_Employee.setRowCount(len(self.employees))
        table_row = 0
        for e in self.employees:
            self.tbl_Employee.setItem(
                table_row, 0, QTableWidgetItem(str(e[0])))
            self.tbl_Employee.setItem(
                table_row, 1, QTableWidgetItem(str(e[1])))
            self.tbl_Employee.setItem(
                table_row, 2, QTableWidgetItem(str(e[2])))
            self.tbl_Employee.setItem(
                table_row, 3, QTableWidgetItem(str(e[4])))
            table_row += 1

    def event_table_employee_was_clicked(self, row, col):
        current_row = self.tbl_Employee.currentRow()
        folder_name = self.tbl_Employee.item(row, 3).text()
        self.event_loadDataset([folder_name])

    def event_loadDataset(self, folder_name):
        self.showDataset_thread.start()
        self.showDataset_thread.folder_names = folder_name
        self.showDataset_thread.ImageUpdate.connect(self.ImageUpdateDataset)

    def event_tranning_data(self):
        if (len(list_folder := self.get_all_folder_dataset()) < 1):
            QMessageBox.warning(
                self, "Warning", "Not have dataset to tranning!", QMessageBox.Ok)
            return
        self.showDataset_thread = LoadDataset_Thread()
        self.showDataset_thread.start()
        self.showDataset_thread.folder_names = list_folder
        self.showDataset_thread.ImageUpdate.connect(self.ImageUpdateDataset)

        time.sleep(1)
        # Thread tranning
        self.tranning_data()

    def get_all_folder_dataset(self):
        name_dirs = []
        for dir in os.listdir("./data/dataset"):
            name_dirs.append(dir)
        return name_dirs

    def tranning_data(self):
        try:
            name_dirs = []
            paths = []
            detector = cv2.CascadeClassifier(
                "./config/haarcascade_frontalface_default.xml")
            for dir in os.listdir("./data/dataset"):
                print(dir)
                name_dirs.append(dir)
            for name in name_dirs:
                for image in os.listdir(f"./data/dataset/{name}"):
                    # path_str = f"dataset/{name}/{image}"
                    path_str = os.path.join(f".\data\dataset\{name}", image)
                    paths.append(path_str)

            face_store = []
            id_store = []
            # Loop through all img_path in list
            for image_path in paths:
                # Open image in file and convert that img to While and Black
                image = Image.open(image_path).convert("L")
                # Convert that img to matrix using "numpy"
                img_arr = np.array(image, dtype="uint8")

                # Get ID of img from img_path
                tmp_path = str(image_path).replace(".\\", "")
                id = str(tmp_path).split("\\")[3].split("_")[0]

                faces = detector.detectMultiScale(img_arr)
                for (x, y, w, h) in faces:
                    face_store.append(img_arr[y:y+h, x:x+w])
                    id_store.append(int(id))
                print(str(tmp_path).split("\\")[2])

            id_store = np.array(id_store)
            # Call the recognizer
            trainer = cv2.face.LBPHFaceRecognizer_create()
            # Give the faces and ids numpy arrays
            trainer.train(face_store, id_store)
            # Write the generated model to a yml file
            trainer.write("./data/tranning/training.yml")
        except:
            pass
        finally:
            QMessageBox.question(
                self, "Notification", "Tranning Successful!", QMessageBox.Ok)

    def event_stop_all_thread(self):
        self.loopCount = 0
        # self.showDataset_thread.stop()


class LoadDataset_Thread(QThread):
    folder_names = None
    ImageUpdate = pyqtSignal(str)

    def run(self):
        self.ThreadActive = True
        while (self.ThreadActive):
            print(self.folder_names)
            for folder in self.folder_names:
                if not os.path.isdir(f"./data/dataset/{folder}"):
                    print("Notification: Not found folder: " +
                          str(f"{os.getcwd()}/data/dataset/{folder}"))
                    self.stop()
                    return
                for image in os.listdir(f"./data/dataset/{folder}"):
                    path_str = os.path.join(
                        f".\data\dataset\{folder}", image)
                    time.sleep(0.25)
                    self.ImageUpdate.emit(path_str)
            self.stop()

    def stop(self):
        self.ThreadActive = False
