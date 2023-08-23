import os
from datetime import datetime, date
from data import path, schedule


def get_week_day_and_time(audio_name):
    """Returns the day of the week starting from 0 (Monday) and the time of the class"""
    date_and_time = datetime.strptime(audio_name[audio_name.index('20'):audio_name.index('.')], '%Y-%m-%d %H-%M-%S')
    subject_week_day = date.strftime(date_and_time, '%A')
    subject_time = date_and_time.time()
    return subject_week_day, subject_time


def string_to_time(string):
    """Returns a time object from a string"""
    return datetime.strptime(string, '%H:%M').time()


def get_right_path(main_path, s_week_day, s_time):
    """Returns the right path to the audio file"""
    for day in schedule:
        if day == s_week_day:
            for subject in schedule[day]:
                if string_to_time(subject['start_time']) <= s_time <= string_to_time(subject['end_time']):
                    return f"{main_path}/{subject['name']}"


def organize(path, file_name):
    """Organizes the audio file in the right folder"""
    print(f""""{file_name}" is being organized...""")
    subject_week_day, subject_time = get_week_day_and_time(file_name)
    subject_full_path = get_right_path(path, subject_week_day, subject_time)
    if subject_full_path is not None:
        try:
            os.rename(f"{path}/{file_name}", f"{subject_full_path}/{file_name}")
        except FileNotFoundError:
            print(f"{subject_full_path} does not exist. Creating folder...")
            os.mkdir(subject_full_path)
            os.rename(f"{path}/{file_name}", f"{subject_full_path}/{file_name}")
        finally:
            print(f""""{file_name}" was organized! and moved to {subject_full_path}/{file_name}""")
    elif subject_full_path is None:
        print(f""""{file_name}" was not organized because it is not in the schedule.""")
