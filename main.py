import os
from datetime import datetime, date, time
from data import path, schedule


def get_week_day_and_time(audio_name):
    """Returns the day of the week starting from 0 (Monday) and the time of the class"""
    date_and_time = datetime.strptime(audio_name[audio_name.index('20'):audio_name.index('.')], '%Y-%m-%d %H-%M-%S')
    subject_week_day = date.strftime(date_and_time, '%A')
    subject_time = date_and_time.time()
    return subject_week_day, subject_time


def string_to_time(string):
    return datetime.strptime(string, '%H:%M').time()


def get_right_path(main_path, s_week_day, s_time):
    """Returns the right path to the audio file"""
    for day in schedule:
        if day == s_week_day:
            for subject in schedule[day]:
                if string_to_time(subject['start_time']) <= s_time <= string_to_time(subject['end_time']):
                    return f"{main_path}/{subject['name']}"


for record_txt in os.listdir(path):
    if os.path.isfile(f"{path}/{record_txt}") and ".txt" in record_txt:
        subject_week_day, subject_time = get_week_day_and_time(record_txt)
        subject_full_path = get_right_path(path, subject_week_day, subject_time)
        