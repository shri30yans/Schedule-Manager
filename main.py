# importing libraries
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime

# importing classes
from database import databaseClass
from reminder import reminderClass

# Creating a database object
databaseObj = databaseClass()
databaseObj.intialize()

# Resetting old Notification statuses
databaseObj.clear_notification_status()
reminderObj = reminderClass(databaseObj)
reminderObj.load_schedule()

# Creating and starting a separate thread for checking the schedule
t = threading.Thread(target=reminderObj.check_schedule)
t.start()

root = tk.Tk()  # Creating Tk object
root.title("Schedule manager")
root.geometry("720x300")  # Adjust size of window
menu = tk.Menu(root)  # Creating a menu
root.config(menu=menu)  # Setting the menu as the menu of our Tk object
root.iconbitmap("icon.ico")  # Setting the top icon of the window


class AddEventFrame:
    def __init__(self, root, databaseObj):
        self.databaseObj = databaseObj

        self.frame = tk.Frame(root, width=800, height=600)
        self.main = tk.Label(
            self.frame, text="Add an event to the schedule.", font="Helvetica 12 bold"
        )

        self.subject = tk.Label(self.frame, text="Subject")
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        self.dropdownchoosen = tk.StringVar()
        today = datetime.today().strftime("%A")  # returns a string of the day name
        self.dropdownchoosen.set(today)

        self.day = tk.Label(self.frame, text="Day")
        self.start_time = tk.Label(self.frame, text="Start time (24h)")
        self.end_time = tk.Label(self.frame, text="End Time (24h)")

        self.subject_textbox = tk.Text(self.frame, height=2, width=50)
        self.daydropdown = tk.OptionMenu(self.frame, self.dropdownchoosen, *days)
        self.daydropdown.config(width=60)
        self.start_time_textbox = tk.Text(self.frame, height=1, width=50)
        self.end_time_textbox = tk.Text(self.frame, height=1, width=50)

        self.btn = ttk.Button(self.frame, text="Submit", command=self.clicked, width=50)

    def SetFrame(self):
        self.hide_all_frames()
        self.frame.grid(row=0, column=0)
        self.main.grid(row=0, column=1, padx=(10, 30), pady=(10, 20))
        for index, x in enumerate(
            [self.subject, self.day, self.start_time, self.end_time]
        ):
            x.grid(row=index + 1, column=0, padx=(90, 10), pady=(10, 0))
        for index, x in enumerate(
            [
                self.subject_textbox,
                self.daydropdown,
                self.start_time_textbox,
                self.end_time_textbox,
            ]
        ):
            x.grid(row=index + 1, column=1, padx=(5, 60), pady=(10, 0))

        self.btn.grid(row=5, column=1, padx=(5, 70), pady=(20, 10))

    def hide_all_frames(self):
        RemoveEventFrameObj.frame.grid_forget()
        ViewTimeTableFrameObj.frame.grid_forget()
        AddEventFrameObj.frame.grid_forget()
        HomeFrameObj.frame.grid_forget()

    def clicked(self):
        subject = self.subject_textbox.get(1.0, "end-1c")
        day = self.dropdownchoosen.get()
        start_time = self.start_time_textbox.get(1.0, "end-1c")
        end_time = self.end_time_textbox.get(1.0, "end-1c")

        # Checking the input inside the text boxes
        for x in [subject, day, start_time, end_time]:
            if len(x.replace(" ", "")) == 0:
                messagebox.showerror(
                    "Python Error", f"Error: One or more textbox is empty."
                )
                return

        for x in [start_time, end_time]:
            time = x.split(":")

            for y in time:
                try:
                    int(y)
                except:
                    messagebox.showerror(
                        "Python Error",
                        f'Error: The hours or minutes are not integers. Use the format "hour:minutes" (24h)',
                    )
                    return

            if ":" not in x:  # Check format
                messagebox.showerror(
                    "Python Error",
                    f'Error: Enter the time in the format "hour:minutes" (24h). You are missing the ":"',
                )
                return

            elif len(time) != 2:  # Check for hours, minutes
                messagebox.showerror(
                    "Python Error",
                    f'Error: Enter the time in the format "hour:minutes" (24h).',
                )
                return

            elif int(time[0]) > 24:  # Hour limits
                messagebox.showerror(
                    "Python Error", f"Error: The hours cannot be more than 24."
                )
                return

            elif int(time[0]) < 0:  # Hour limits
                messagebox.showerror(
                    "Python Error", f"Error: The hours cannot be less than 0."
                )
                return

            elif int(time[1]) > 60:  # Minutes limits
                messagebox.showerror(
                    "Python Error", f"Error: The minutes cannot be more than 60."
                )
                return

            elif int(time[1]) < 0:  # Minutes limits
                messagebox.showerror(
                    "Python Error", f"Error: The minutes cannot be less than 0."
                )
                return

        if int(start_time.split(":")[0]) > int(end_time.split(":")[0]) or int(
            start_time.split(":")[1]
        ) > int(end_time.split(":")[1]):
            messagebox.showerror(
                "Python Error", f"Error: The start time cannot be after the end time."
            )
            return

        def format_time(string):
            """
            Remove all special characters and add ":00" to the time
            """
            newstring = ""
            for x in string:
                if x.isnumeric:
                    newstring += x
                elif x == ":":
                    newstring += x
                else:
                    pass
            newstring += ":00"
            return newstring

        start_time = format_time(start_time)
        end_time = format_time(end_time)

        status = self.databaseObj.add_event(
            subject=subject, day=day, start_time=start_time, end_time=end_time
        )

        if status is not None:
            # An error was raised
            messagebox.showerror("Python Error", f"{status}")

        # Clearing the text boxes
        self.subject_textbox.delete("1.0", "end")
        self.start_time_textbox.delete("1.0", "end")
        self.end_time_textbox.delete("1.0", "end")

        # Reload the schedule for reminders
        reminderObj.load_schedule()


class RemoveEventFrame:
    def __init__(self, root, databaseObj):
        self.databaseObj = databaseObj

        self.frame = tk.Frame(root, width=800, height=600)
        self.main = tk.Label(
            self.frame,
            text="Remove an event from the schedule.",
            font="Helvetica 12 bold",
        )

        self.event_to_remove = tk.Label(self.frame, text="Event ID to remove")
        self.event_to_remove_textbox = tk.Text(self.frame, height=1, width=50)

        self.btn = ttk.Button(
            self.frame, text="Remove event", command=self.clicked, width=50
        )

    def SetFrame(self):
        self.hide_all_frames()
        self.frame.grid(row=0, column=0)
        self.main.grid(row=0, column=1, padx=(10, 30), pady=(10, 20))
        self.event_to_remove.grid(row=1, column=0, padx=(90, 10), pady=(10, 0))
        self.event_to_remove_textbox.grid(row=1, column=1, padx=(5, 60), pady=(10, 0))
        self.btn.grid(row=2, column=1, padx=(5, 70), pady=(20, 10))

    def hide_all_frames(self):
        RemoveEventFrameObj.frame.grid_forget()
        ViewTimeTableFrameObj.frame.grid_forget()
        AddEventFrameObj.frame.grid_forget()
        HomeFrameObj.frame.grid_forget()

    def clicked(self):
        id = self.event_to_remove_textbox.get(1.0, "end-1c")
        try:
            id = int(id)
        except TypeError:
            messagebox.showerror("Python Error", f"Error: {id} is not a integer.")
            return

        self.databaseObj.delete_event(id)
        self.event_to_remove_textbox.delete("1.0", "end")

        # Reload the schedule for reminders
        reminderObj.load_schedule()


class ViewTimeTableFrame:
    def __init__(self, root, databaseObj):
        self.databaseObj = databaseObj
        self.frame = tk.Frame(root, width=800, height=600)

    def SetFrame(self):
        self.hide_all_frames()
        self.frame.grid(row=0, column=0)
        data = self.databaseObj.get_schedule()
        if data == []:
            self.clear_frame()
            self.label = tk.Label(
                self.frame,
                text='There are no events yet. Add some events from the "Add Events Menu".',
                font="Helvetica 12 bold",
            )
            self.label.grid(row=0, column=0, padx=(90, 90), pady=(20, 20))

        else:
            self.clear_frame()
            for index, x in enumerate(
                [
                    "Subject",
                    "Day",
                    "Start Time (24h)",
                    "End Time (24h)",
                    "ID",
                ]
            ):
                e = tk.Entry(
                    self.frame, width=20, font="Calibri 10 bold", justify="center"
                )
                e.grid(row=0, column=index)
                e.insert(tk.END, x)
                # Set the entries to be non-editable
                e.config(state="readonly")

            row_number = 1
            for row in data:
                for index, cell_data in enumerate(row):
                    e = tk.Entry(self.frame, width=20, font="Calibri 10")
                    e.grid(row=row_number, column=index)
                    e.insert(tk.END, cell_data)
                    # Set the entries to be non-editable
                    e.config(state="readonly")
                row_number += 1

    def clear_frame(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def hide_all_frames(self):
        ViewTimeTableFrameObj.frame.grid_forget()
        RemoveEventFrameObj.frame.grid_forget()
        AddEventFrameObj.frame.grid_forget()
        HomeFrameObj.frame.grid_forget()


class HomeFrame:
    def __init__(
        self,
        root,
    ):
        self.frame = tk.Frame(root, width=800, height=600)
        self.main = tk.Label(
            self.frame,
            text="Choose an option from the menu to get started.",
            font="Helvetica 12 bold",
        )

    def SetFrame(self):
        self.hide_all_frames()
        self.frame.grid(row=0, column=0)
        self.main.grid(row=0, column=0, padx=(90, 90), pady=(20, 20))

    def hide_all_frames(self):
        RemoveEventFrameObj.frame.grid_forget()
        ViewTimeTableFrameObj.frame.grid_forget()
        AddEventFrameObj.frame.grid_forget()
        HomeFrameObj.frame.grid_forget()


# Creating Frame objects from the classes
HomeFrameObj = HomeFrame(root=root)
AddEventFrameObj = AddEventFrame(root=root, databaseObj=databaseObj)
RemoveEventFrameObj = RemoveEventFrame(root=root, databaseObj=databaseObj)
ViewTimeTableFrameObj = ViewTimeTableFrame(root=root, databaseObj=databaseObj)

# Setting the HomeFrame when the program opens.
HomeFrameObj.SetFrame()


# Create a menu item
file_menu = tk.Menu(menu)
# Creating a sub menu by associating it with our parent menu
menu.add_cascade(label="Menu", menu=file_menu)
file_menu.add_command(label="Add an event", command=AddEventFrameObj.SetFrame)
file_menu.add_command(label="Remove an event", command=RemoveEventFrameObj.SetFrame)
file_menu.add_command(label="View Timetable", command=ViewTimeTableFrameObj.SetFrame)

root.mainloop()
