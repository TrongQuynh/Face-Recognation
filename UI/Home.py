from PyQt5.QtWidgets import QMainWindow, QMessageBox, QGraphicsDropShadowEffect
from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from Query import Query
from model.Employee import Employee
from UI.NewEmployee import UI_New_Employee
from UI.EmployeeList import UI_Employee_List
from UI.Department import Department
from UI.Timekeeping import Timekeeping
from UI.TimekeepingRecord import Timekeeping_Record
from UI.Tranning import Tranning


class Home(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/Home.ui", self)

        self.current_form = "Home"
        self.current_UI = self

        self.WiDTH_WINDOWN = 1500
        self.HEIGHT_WINDOWN = 800

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.UI_addEmployee = UI_New_Employee()
        self.UI_employeeList = UI_Employee_List()
        self.UI_department = Department()
        self.UI_Timekeeping = Timekeeping()
        self.UI_TKRecord = Timekeeping_Record()
        self.UI_Tranning = Tranning()

        self.lbl_background.setPixmap(
            QPixmap("./public/img/BackgroungHome.jpg"))
        # QPixmap("./public/img/employee-background.jfif"))

        self.pushButton_8.clicked.connect(
            lambda: self.event_change_form("newEmployee"))
        self.pushButton_11.clicked.connect(
            lambda: self.event_change_form("employee"))
        self.pushButton_14.clicked.connect(
            lambda: self.event_change_form("department"))
        self.pushButton_17.clicked.connect(
            lambda: self.event_change_form("timekeeping"))
        self.pushButton_3.clicked.connect(
            lambda: self.event_change_form("timekeeping-record"))
        self.pushButton_20.clicked.connect(
            lambda: self.event_change_form("tranning"))

        # event back to home page
        self.UI_employeeList.btn_Back.mousePressEvent = self.event_back_to_home
        self.UI_addEmployee.btn_Back.mousePressEvent = self.event_back_to_home
        self.UI_Timekeeping.btn_Back.mousePressEvent = self.event_back_to_home
        self.UI_department.btn_Back.mousePressEvent = self.event_back_to_home
        self.UI_TKRecord.btn_Back.mousePressEvent = self.event_back_to_home
        self.UI_Tranning.btn_Back.mousePressEvent = self.event_back_to_home

        # event close app
        self.UI_employeeList.lbl_Close.mousePressEvent = self.event_close_app
        self.UI_addEmployee.lbl_Close.mousePressEvent = self.event_close_app
        self.UI_Timekeeping.lbl_Close.mousePressEvent = self.event_close_app
        self.UI_department.lbl_Close.mousePressEvent = self.event_close_app
        self.UI_TKRecord.lbl_Close.mousePressEvent = self.event_close_app
        self.UI_Tranning.lbl_Close.mousePressEvent = self.event_close_app
        self.lbl_Close.mousePressEvent = self.event_close_app

        # event minimize app
        self.lbl_Minimize.mousePressEvent = self.event_minimize_app

        # css header form
        self.shadow = QGraphicsDropShadowEffect()

        # setting blur radius
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QtGui.QColor(0, 153, 153).lighter())
        self.shadow.setOffset(5)

    def event_change_form(self, form):
        self.current_form = form

        if (form == "newEmployee"):
            self.current_UI = self.UI_addEmployee
        elif (form == "employee"):
            self.current_UI = self.UI_employeeList
        elif (form == "department"):
            self.current_UI = self.UI_department
        elif (form == "timekeeping"):
            self.current_UI = self.UI_Timekeeping
        elif (form == "timekeeping-record"):
            self.current_UI = self.UI_TKRecord
        elif (form == "tranning"):
            self.current_UI = self.UI_Tranning

        self.current_UI.setFixedHeight(self.HEIGHT_WINDOWN)
        self.current_UI.setFixedWidth(self.WiDTH_WINDOWN)
        self.current_UI.setWindowFlag(Qt.FramelessWindowHint)
        self.current_UI.show()
        self.current_UI.init_form()
        self.hide()

    def event_back_to_home(self, *arg, **kwargs):

        if (self.current_form == "timekeeping"):
            self.UI_Timekeeping.event_stop_all_thread()
            self.UI_Timekeeping.hide()
        elif (self.current_form == "tranning"):
            self.UI_Tranning.hide()
            self.UI_Tranning.event_stop_all_thread()
        elif (self.current_form == "newEmployee"):
            self.UI_addEmployee.hide()
            self.UI_addEmployee.event_stop_all_thread()
        elif (self.current_form == "employee"):
            self.UI_employeeList.hide()
            self.UI_employeeList.event_stop_all_thread()

        self.UI_department.hide()
        self.UI_TKRecord.hide()

        self.current_UI = self
        self.current_form = "Home"
        self.show()

    def event_close_app(self, *arg, **kwargs):
        mess = QMessageBox()
        mess.setWindowTitle("Warning")
        mess.setText("Are you sure want to close application ?")

        mess.setIcon(QMessageBox.Warning)
        mess.setWindowIcon(QtGui.QIcon("./public/img/back.png"))
        mess.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if mess.exec_() == QMessageBox.Yes:
            self.current_UI.close()

    def event_minimize_app(self, *arg, **kwargs):
        self.current_UI.showMinimized()
