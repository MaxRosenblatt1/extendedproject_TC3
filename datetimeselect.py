import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class DateSelector:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Custom style for the calendar widget
        style = ttk.Style(self.master)
        style.theme_use('default')
        style.configure('Calendar.TButton', font=('Arial', 10))
        style.configure('Calendar.Treeview', foreground='black', background='white')
        style.configure('Calendar.Header', foreground='black', font=('Arial', 12, 'bold'))
        style.configure('Calendar.Cell', foreground='black', font=('Arial', 10))
        style.map('Calendar.TButton', background=[('active', 'grey')])

        # Date picker
        self.date_label = tk.Label(self.frame, text="Select a date:")
        self.date_label.pack()
        self.cal = Calendar(self.frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, selectbackground='grey', selectforeground='black')
        self.cal.pack()

        # Time picker
        self.time_label = tk.Label(self.frame, text="Select a time:")
        self.time_label.pack()
        self.time_entry = tk.Entry(self.frame)
        self.time_entry.insert(0, datetime.now().strftime("%H:%M:%S"))
        self.time_entry.pack()

        # OK button
        self.ok_button = tk.Button(self.frame, text="OK", command=self.get_selection)
        self.ok_button.pack()

        #Now button

        self.now_button = tk.Button(self.frame, text="Now", command=self.set_to_now)
        self.now_button.pack()

        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None


    def set_to_now(self):
        now = datetime.now()
        self.cal.selection_set(now.date())
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, now.strftime("%H:%M:%S"))


    def get_selection(self):
        date_obj = self.cal.selection_get()
        self.year = date_obj.year
        self.month = date_obj.month
        self.day = date_obj.day
        time_str = self.time_entry.get()
        try:
            hour, minute, second = map(int, time_str.split(':'))
        except ValueError:
            hour = int(time_str)
            minute = 0
            second = 0
        if minute < 0 or minute > 59:
            raise ValueError("Invalid minute value")
        if second < 0 or second > 59:
            raise ValueError("Invalid second value")
        self.hour = hour
        self.minute = minute
        self.second = second
        if self.minute == 00 and self.second == 00:
            self.minute = self.second = 00

        self.master.quit()

def select_date_and_time():
    root = tk.Tk()
    app = DateSelector(root)
    root.mainloop()
    return app.year, app.month, app.day, app.hour, app.minute, app.second

