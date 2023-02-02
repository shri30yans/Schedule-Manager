import mysql.connector as m
from datetime import datetime


class databaseClass:
    def __init__(self):
        self.conn = self.connection()

    def connection(self):
        # if localhost is not working 127.0.0.1
        conn = m.connect(host="localhost", user="root", password="Welcome1")
        if conn.is_connected():
            print("Database Connection is succesful.")
        return conn

    def intialize(self):
        """
        Setting up the Database
        """
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS schedule_db")
        self.conn.commit()
        self.cursor.execute("USE schedule_db")
        self.conn.commit()

        # self.cursor.execute("DROP TABLE IF EXISTS schedule")
        # self.conn.commit()

        self.cursor.execute(
            """
                    CREATE TABLE IF NOT EXISTS schedule
                    (
                    id INTEGER (10) AUTO_INCREMENT PRIMARY KEY,
                    subject VARCHAR (255),
                    day VARCHAR (10),
                    start_time TIME,
                    end_time TIME,
                    notification_status VARCHAR(1)
                    )
                    """
        )
        self.conn.commit()

    def get_schedule(self):
        """
        Gets the schedule of all the days according to the days of the week.
        """
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        data = []
        for x in days:
            query = f"SELECT subject,day,start_time,end_time,id FROM schedule WHERE day = '{x}' ORDER BY start_time ASC"
            self.cursor.execute(query)
            data.extend(self.cursor.fetchall())
        return data

    def delete_event(self, id):
        """
        Deletes a event through it's id
        """
        query = f"DELETE FROM schedule WHERE id = {id}"
        self.cursor.execute(query)
        self.conn.commit()

    def change_notification_status(self, status, id):
        """
        Changes the notification_status of a particular event
        Possible statuses:
            1) N : Not notified
            2) S : Notified about Start time
            3) E : Notified about End time
        """
        query = f"UPDATE schedule SET notification_status = '{status}' WHERE id = {id}"
        self.cursor.execute(query)
        self.conn.commit()

    def clear_notification_status(self):
        """
        Sets all the notification status to N (Not notified) for a particular day
        """
        today = datetime.today().strftime("%A")  # returns a string of the day name
        query = f"UPDATE schedule SET notification_status = 'N' WHERE day = '{today}'"
        self.cursor.execute(query)
        self.conn.commit()

    def get_current_day_schedule(self):
        """
        Get's the schedule of a particular day in the format:
            [(subject,start_time,end_time,id,notification_status),(subject,start_time,end_time,id,notification_status)]
        """
        today = datetime.today().strftime("%A")  # returns a string of the day name
        query = f"SELECT subject,start_time,end_time,id,notification_status FROM schedule WHERE day = '{today}' ORDER BY start_time ASC"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def add_event(self, subject, day, start_time, end_time):
        """
        Adding an event into the schedule
        """
        try:
            query = f"INSERT INTO schedule(subject,day,start_time,end_time,notification_status) VALUES('{subject}','{day}','{start_time}','{end_time}','N')"
            self.cursor.execute(query)
            self.conn.commit()
        except m.errors.DataError as e:
            return e
