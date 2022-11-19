from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

import sys

from Query import Query
from model.Employee import Employee


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Login.ui", self)
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.lbl_background1.setPixmap(QPixmap("./public/img/moutain.jpg"))
        self.btn_Close.setPixmap(QPixmap("./public/img/close.png"))
        self.btn_Close.mousePressEvent = self.event_Close

        self.txt_Username.setText("admin")
        self.txt_Pwd.setText("123")

    def event_Close(self, *arg, **kwargs):
        self.close()

    def check_Login(self):
        username = self.txt_Username.text()
        pwd = self.txt_Pwd.text()
        if (str(username) == "admin" and str(pwd) == "123"):
            return True
        return False
