from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QTableWidgetItem, QTableView
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.QtCore import QRect, QPropertyAnimation, QDate
from threading import Thread
from Query import Query

from datetime import date, datetime
from calendar import monthrange


class Timekeeping_Record(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./UI/TimekeepingRecord.ui", self)
        self.center()
        self.btn_Back.setPixmap(QPixmap("./public/img/back.png"))
        self.lbl_Background.setPixmap(
            QPixmap("./public/img/backgroundColor.jfif"))
        self.intit_table()

    def init_form(self):

        print("Hello")
        self.current_employeeID = None
        self.cbox_Department.setCurrentIndex(0)

        # QSpinBox Month
        self.spinBox_Month.setMinimum(1)
        self.spinBox_Month.setMaximum(12)
        self.spinBox_Month.setValue(datetime.today().month)

        # QSpinBox YEAR
        self.spinBox_Year.setMinimum(1999)
        self.spinBox_Year.setMaximum(datetime.today().year)
        self.spinBox_Year.setValue(datetime.today().year)

        # QDateEdit filter by date
        self.dateEdit.setDate(QDate.currentDate())

        self.init_throughScreenText()

        # show data for employee table
        self.load_data_employee_table(Query().select_All_Employee())

        # Load data for combobox
        self.load_data_cbox_Department()

        # Event combo box change value
        self.cbox_Department.currentIndexChanged.connect(
            self.event_filter_e_by_department)

        # event click
        self.btn_Search_Employee.clicked.connect(self.event_filter_employee)

        self.btn_Refresh.clicked.connect(self.event_Refresh)

        self.tbl_Employee.cellClicked.connect(
            self.event_load_data_for_timekeeping_table)

        self.dateEdit.dateChanged.connect(self.event_filter_TKRecord_by_date)

        self.btn_Refresh_2.clicked.connect(self.event_Refresh_TK_table)

        self.spinBox_Month.valueChanged.connect(
            self.event_filter_TKRecord_by_month_Year)

        self.spinBox_Year.valueChanged.connect(
            self.event_filter_TKRecord_by_month_Year)

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

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def intit_table(self):
        # Remove index of table
        self.tbl_Employee.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Employee.verticalHeader().setVisible(False)

        self.tbl_Employee.setColumnWidth(0, 50)
        self.tbl_Employee.setColumnWidth(1, 110)
        self.tbl_Employee.setColumnWidth(2, 120)
        self.tbl_Employee.setColumnWidth(3, 120)
        self.tbl_Employee.setColumnWidth(4, 120)
        self.tbl_Employee.setHorizontalHeaderLabels(
            ["ID", "Full Name", "Phone Number", "Email", "Department"])

        self.tbl_Timekeeping.setSelectionBehavior(QTableView.SelectRows)
        self.tbl_Timekeeping.verticalHeader().setVisible(False)
        self.tbl_Timekeeping.setColumnWidth(0, 150)
        self.tbl_Timekeeping.setColumnWidth(1, 120)
        self.tbl_Timekeeping.setColumnWidth(2, 120)
        self.tbl_Timekeeping.setColumnWidth(3, 100)
        self.tbl_Timekeeping.setHorizontalHeaderLabels(
            ["Date", "Time In", "Time Out", "Hours"])

    def event_filter_TKRecord_by_date(self):
        if (self.current_employeeID == None):
            return
        date = self.dateEdit.date().toString("yyyy/MM/dd")
        data = Query().select_All_TKRecord_in_range_a_employee(
            self.current_employeeID, date)
        self.load_data_timekeeping_table(data)

    def event_filter_TKRecord_by_month_Year(self):
        if (self.current_employeeID == None):
            return
        month = self.spinBox_Month.value()
        year = self.spinBox_Year.value()
        data = Query().select_TKRecord_an_employee_by_Month_Year(
            self.current_employeeID, month, year)
        self.TotalHourWork = 0
        self.load_data_timekeeping_table(data)
        self.event_load_info()

    def event_load_info(self):
        self.load_data_info_Year()
        self.load_data_info_Month()
        self.load_total_day_not_work_in_month()

    def event_Refresh(self):
        self.load_data_employee_table(Query().select_All_Employee())

    def event_Refresh_TK_table(self):
        data = Query().select_All_TKRecord_by_EmployeeID(self.current_employeeID)
        self.load_data_timekeeping_table(data)

    def event_load_data_for_timekeeping_table(self, row, col):
        e_id = self.tbl_Employee.item(row, 0).text()
        data = Query().select_All_TKRecord_by_EmployeeID(e_id)

        self.current_employeeID = e_id
        self.TotalDayWork = len(data)
        self.TotalHourWork = 0

        self.load_data_timekeeping_table(data)
        self.load_data_info_area()
        self.event_load_info()

    # Load Data

    def load_data_cbox_Department(self):
        self.cbox_Department.clear()
        departments = Query().select_All_Department()
        self.cbox_Department.addItem("None")
        for d in departments:
            self.cbox_Department.addItem(d[1])

    def load_data_employee_table(self, employees):
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

    def load_data_timekeeping_table(self, data):
        table_row = 0
        self.tbl_Timekeeping.setRowCount(len(data))
        for d in data:
            # datetime = datetime.strptime(date_string, '%Y-%m-%d')
            # print(type(d[2]))
            hours = 0
            if (d[3] is not None):
                hour_in = (datetime.strptime(str(d[2]), "%H:%M:%S")).hour
                hour_out = (datetime.strptime(str(d[3]), "%H:%M:%S")).hour
                hours = hour_out - hour_in

            self.tbl_Timekeeping.setItem(
                table_row, 0, QTableWidgetItem(str(d[1])))
            self.tbl_Timekeeping.setItem(
                table_row, 1, QTableWidgetItem(str(d[2])))
            self.tbl_Timekeeping.setItem(
                table_row, 2, QTableWidgetItem(str(d[3])))
            self.tbl_Timekeeping.setItem(
                table_row, 3, QTableWidgetItem(str(hours)))

            table_row += 1

            self.TotalHourWork = self.TotalHourWork + hours

    def is_number(self, number):
        try:
            int(number)
            return True
        except:
            return False

    def event_filter_employee(self):
        employees = Query().select_All_Employee()
        employee_list = []
        text_search = self.txt_Search_Employee.text()
        if (self.is_number(text_search)):
            for e in employees:
                if e[0] == int(text_search):
                    employee_list.append(e)

        else:
            for e in employees:
                e_FName = str(e[1]).replace(" ", "").lower()
                search_FName = str(text_search).replace(" ", "").lower()
                if search_FName in e_FName or e_FName in search_FName:
                    employee_list.append(e)
        self.load_data_employee_table(employee_list)

    def event_filter_e_by_department(self):
        print(self.cbox_Department.currentIndex())
        if (self.cbox_Department.currentIndex() < 1):
            return
        department_name = str(self.cbox_Department.currentText())
        department_id = Query().select_Department_by_Name(department_name)[0]

        employees = Query().select_Employee_by_department_ID(department_id)
        self.load_data_employee_table(employees)

    def event_stop_all_thread(self):
        self.loopCount = 0

    def load_data_info_area(self):

        self.txt_EmployeeName.setText(
            Query().select_Employee_by_ID(self.current_employeeID)[1])
        self.txt_TotalDayWork.setText(str(self.TotalDayWork))
        self.txt_TotalHourWork.setText(str(self.TotalHourWork))

    def getTotalHours(self, TK_List):
        count = 0
        for d in TK_List:
            hours = 0
            if (d[3] is not None):
                hour_in = (datetime.strptime(str(d[2]), "%H:%M:%S")).hour
                hour_out = (datetime.strptime(str(d[3]), "%H:%M:%S")).hour
                hours = hour_out - hour_in
            count = count + hours
        return count

    def getTotalGoLate(self, TK_List):
        TIME_IN = 7
        count = 0
        for tk in TK_List:
            hour_in = (datetime.strptime(str(tk[2]), "%H:%M:%S")).hour
            minute_in = (datetime.strptime(str(tk[2]), "%H:%M:%S")).minute
            if (hour_in >= TIME_IN and minute_in > 0):
                count = count + 1
        return count

    def getTotalLeaveEarly(self, TK_List):
        TIME_OUT = 18
        count = 0
        for tk in TK_List:
            hour_out = (datetime.strptime(str(tk[3]), "%H:%M:%S")).hour
            if (hour_out < TIME_OUT):
                count = count + 1
        return count

    def load_data_info_Year(self):
        data = Query().select_TKRecord_an_employee_by_Year(
            self.current_employeeID, self.spinBox_Year.value())
        self.txt_CurrentYear.setText(str(self.spinBox_Year.value()))
        self.txt_TotalHourWork_Year.setText(str(self.getTotalHours(data)))

    def load_data_info_Month(self):
        month = self.spinBox_Month.value()
        year = self.spinBox_Year.value()
        data = Query().select_TKRecord_an_employee_by_Month_Year(
            self.current_employeeID, month, year)
        self.txt_CurrentMonth.setText(
            str(f"{self.spinBox_Month.value()} - {self.spinBox_Year.value()}"))
        self.txt_TotalHourWork_Month.setText(str(self.getTotalHours(data)))
        self.txt_TotalTimeGoLate.setText(str(self.getTotalGoLate(data)))
        self.txt_TotalTimeLeaveEarly.setText(
            str(self.getTotalLeaveEarly(data)))

    def get_total_day_not_work_in_year(self):
        result = 0
        year = self.spinBox_Year.value()
        for month in range(1, 13):
            num_day_worked = len(Query().select_TKRecord_an_employee_by_Month_Year(
                self.current_employeeID, month, year))
            num_days = monthrange(year, month)[1]  # num_days = 28
            result = result + (num_days - num_day_worked)
        return

    def load_total_day_not_work_in_month(self):
        # get total day not work in Month
        month = self.spinBox_Month.value()
        year = self.spinBox_Year.value()
        num_day_worked = len(Query().select_TKRecord_an_employee_by_Month_Year(
            self.current_employeeID, month, year))
        # Current Month
        if (date.month == month and date.year == year):
            days = datetime.now().day
        # Old Month
        else:
            days = monthrange(year, month)[1]
        self.txt_TotalDayNotWork.setText(str(days - num_day_worked))
