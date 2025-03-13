# %%
from datetime import time, timedelta, datetime

FULL_DAY = 0
MORNING = 1
MORNING_LUNCH = 2
AFTERNOON = 3

class TimeCalculator:
    def __init__(self):
        self.start_time: time = datetime.now().time()
        self.late: timedelta = None
        self.time_type = FULL_DAY
        self.end_time: time = None

    def set_start_time(self, hour: int, minute: int):
        if 0 <= hour < 24 and 0 <= minute < 60:
            if hour < 7:
                self.start_time = time(7, 0)
            elif hour > 18:
                self.start_time = time(18, 48)
            else:
                self.start_time = time(hour, minute)
            print(f"Start time set to: {self.start_time.strftime('%H:%M')}")
        else:
            raise ValueError("Invalid hour or minute. Hour must be between 0-23 and minute between 0-59.")

    def cal_late(self, type=FULL_DAY):
        if self.start_time is None:
            raise ValueError("You need to set the start time before calculating the full time end.")
        valid_time = time(9, 0)
        if type == AFTERNOON:
            valid_time = time(13, 0)
        print(valid_time)
        if self.start_time > valid_time:
            valid_minutes = valid_time.hour * 60 + valid_time.minute
            start_minutes = self.start_time.hour * 60 + self.start_time.minute
            self.late = timedelta(minutes=start_minutes - valid_minutes)
            print(f"Late by: {self.late}")
        else:
            self.late = timedelta(0)
            print("Not late.")

    def add_time(self, base_time: time, hours: int, minutes: int) -> time:
        """Helper method to add hours and minutes to a time object."""
        total_minutes = base_time.hour * 60 + base_time.minute + hours * 60 + minutes
        total_minutes %= 24 * 60  # Ensure the time wraps around 24 hours
        return time(total_minutes // 60, total_minutes % 60)

    def process_time_over(self):
        lastest_time = time(18, 48)
        if self.end_time > lastest_time:
            self.end_time = lastest_time

    def cal_end_time(self, type=FULL_DAY):
        self.cal_late(type)
        if type == MORNING:
            work_hours = 4
            work_minutes = 24
        elif type == MORNING_LUNCH:
            work_hours = 5
            work_minutes = 24
        elif type == AFTERNOON:
            self.end_time = time(5, 24)
            return self.end_time.strftime('%H:%M')
        else:
            work_hours = 9
            work_minutes = 48
        self.end_time = self.add_time(self.start_time, work_hours, work_minutes)
        self.process_time_over()
        return self.end_time.strftime('%H:%M')


