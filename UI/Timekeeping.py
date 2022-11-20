import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2
import os
import time


class Timekeeping(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Timekeeping.ui", self)
        self.center()
        self.recognize_thread = Recognize_thread()

        self.recognize_thread.start()
        self.recognize_thread.ImageUpdate.connect(self.ImageUpdateSlot)
        # self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ImageUpdateSlot(self, Image):
        self.lbl_Capture.setPixmap(QPixmap.fromImage(Image))


class Recognize_thread(QThread):
    ImageUpdate = pyqtSignal(QImage)
    face_cascaded = cv2.CascadeClassifier(
        "./config/haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./data/tranning/training.yml")

    start_time = 0
    names = {}

    for user in os.listdir("./data/dataset/"):
        id = int(os.listdir(f"./data/dataset/{user}")[0].split('_')[0])
        names[id] = user

    def run(self):

        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()

            # Flip Image
            frame = cv2.flip(frame, 1)

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
                # confidence_format = f"{int(confidence)} %"
                confidence_format = "  {0}%".format(round(100 - confidence))
                print(id, confidence)
                if (confidence < 100):
                    pass
                else:
                    username = "Unknown"
                    # confidence_format = "---"
                cv2.putText(
                    frame, username, (x1, y1), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
                cv2.putText(
                    frame, confidence_format, (x1, y2), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))

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
                Pic = ConvertToQtFormat.scaled(820, 570, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()
