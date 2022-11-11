class Employee:
    def __init__(self, fullname, email, phonenumber, dataset) -> None:
        self.fullname = fullname
        self.email = email
        self.phonenumber = phonenumber
        self.dataset = dataset

    def show_Employee_info(self):
        print(self.fullname + "\n" + self.email + "\n" +
              self.phonenumber + "\n" + self.dataset)
