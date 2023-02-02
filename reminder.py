from datetime import datetime
from tkinter import messagebox
import time

try:
    import pyttsx3
except:
    pass


class reminderClass:
    def __init__(self, databaseObj):
        self.databaseObj = databaseObj

    def load_schedule(self):
        """
        Stores the schedule in a list with the Event information in tuples
        """
        self.schedule = self.databaseObj.get_current_day_schedule()

    def check_schedule(self):
        while True:
            current_time = datetime.now().strftime(f"%H:%M") + ":00"
            for event in self.schedule:
                subject, start_time, end_time, id, notification_status = (
                    event[0],
                    event[1],
                    event[2],
                    event[3],
                    event[4],
                )
                """
                Possible notification statuses:
                    1) N : Not notified
                    2) S : Notified about Start time
                    3) E : Notified about End time
                """

                def check_for_events(notification_status_to_check, time, phrase):
                    # print(notification_status != notification_status_to_check)
                    if notification_status != notification_status_to_check:
                        if str(time) == current_time:
                            print("----------------")
                            print(f"Alert! {subject} time has {phrase}.")

                            for x in range(3):
                                response = self.speak(
                                    f"Alert! {subject} time has {phrase}"
                                )
                                if response == "Error":
                                    break
                                time.sleep(1)

                            messagebox.showinfo(
                                "Alert!",
                                f"{subject} time has {phrase}. Please view the schedule for more details.",
                            )

                            # update notification status
                            self.databaseObj.change_notification_status(
                                status=notification_status_to_check, id=id
                            )
                            print("----------------\n")

                check_for_events("S", start_time, "started")
                check_for_events("E", end_time, "ended")
                time.sleep(5)

    def speak(self, text):
        try:
            # creating an engine instance
            tts_engine = pyttsx3.init()
            voices = tts_engine.getProperty("voices")
            tts_engine.setProperty("voice", voices[1].id)
            # passes input text to be spoken
            tts_engine.say(text)
            # process the voice commands
            tts_engine.runAndWait()
        except:
            print(
                "Looks like the pyttsx3 module isn't installed.\nAudio reminders are not currently working."
            )
            return "Error"
