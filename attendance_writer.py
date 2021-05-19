import csv
import time
import datetime
import os

class Attendance:
    """
    attendance writer class automatically creates date wise attendance record files and keeps track of people who are present
    """
    def __init__(self) -> None:
        self.names = []
        self.attendance_sheet = f"attendance_{datetime.datetime.today().strftime('%d-%m-%Y')}.csv"
        #creating attendance sheet and initializing names
        if self.attendance_sheet in os.listdir():
            with open(self.attendance_sheet, 'r') as f_object:
                csv_reader = csv.reader(f_object, delimiter=',')
                for line in csv_reader:
                    self.names.append(line[0])
        else:
            print("yaha aagaye")
            with open(self.attendance_sheet, 'w') as f_object:
                writer_object = csv.writer(f_object)
                writer_object.writerow(["name", "time"])
                f_object.close()

    def write_attendence(self, name):
        List=[name, time.asctime()]
        if name not in self.names:
            self.names.append(name)
            with open(self.attendance_sheet, 'a') as f_object:
                writer_object = csv.writer(f_object)
                writer_object.writerow(List)
                f_object.close()
