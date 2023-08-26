import os
import re
from datetime import datetime, date
from data import schedule


def get_week_day_and_time(audio_name: str) -> tuple:
    """Returns the day of the week starting from 0 (Monday) and the time of the class"""
    pattern = r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}"
    match = re.search(pattern, audio_name)
    date_and_time = datetime.strptime(match.group(), '%Y-%m-%d %H-%M')
    subject_week_day = date.strftime(date_and_time, '%A')
    subject_time = date_and_time.time()
    return subject_week_day, subject_time


def string_to_time(string: str) -> datetime.time:
    """Returns a time object from a string"""
    return datetime.strptime(string, '%H:%M').time()


def get_right_path(main_path: str, s_week_day: str, s_time: str) -> str:
    """Returns the right path to the audio file"""
    for day in schedule:
        if day == s_week_day:
            for subject in schedule[day]:
                if string_to_time(subject['start_time']) <= s_time <= string_to_time(subject['end_time']):
                    return f"{main_path}/{subject['name']}"
                else:
                    return main_path


def remove_file(file_path: str, file_name: str, ext: str) -> None:
    """Removes file from the path"""
    print(f"""Removing "{file_name}.{ext}"...""")
    os.remove(f"{file_path}/{file_name}.{ext}")
    print(f""""{file_name}.{ext}" was removed!""")


def organize(path: str, file_name: str) -> None:
    """Organizes the audio file in the right folder"""
    subject_week_day, subject_time = get_week_day_and_time(file_name)
    subject_full_path = get_right_path(path, subject_week_day, subject_time)
    if subject_full_path != path:
        print(f""""{file_name}" is being organized...""")
        try:
            os.rename(f"{path}/{file_name}", f"{subject_full_path}/{file_name}")
        except FileNotFoundError:
            print(f""""{subject_full_path}" does not exist. Creating folder...""")
            os.mkdir(subject_full_path)
            os.rename(f"{path}/{file_name}", f"{subject_full_path}/{file_name}")
        finally:
            print(f""""{file_name}" was organized! and moved to {subject_full_path}/{file_name}""")
    else:
        print(f""""{file_name}" was not organized because it is not in the schedule.""")