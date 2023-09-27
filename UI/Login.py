from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap


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
        self.txt_Pwd.setText("admin123")

    def event_Close(self, *arg, **kwargs):
        reply = QMessageBox.question(
            self, "Warning", "Are you sure want to close application ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def check_Login(self):
        username = self.txt_Username.text()
        pwd = self.txt_Pwd.text()
        if (Query().select_Account(username, pwd)):
            return True
        return False
