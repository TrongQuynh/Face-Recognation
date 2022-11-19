from datetime import datetime, date


class TimekeepingRecord:
    def __init__(self, e_id) -> None:
        self.e_id = e_id
        self.date = date.today()
        self.time_in = datetime.now()
        self.time_out = None

    def get_datetime_now():
        return datetime.now()

    def get_time_now(self):
        return datetime.now().strftime("%H:%M:%S")

    def show_info(self):
        print("Employee ID: " + self.e_id+"\nTime: " + self.date + "\n" + "Time in: " +
              self.time_in + "\n" + "Time out: " + self.time_out)
