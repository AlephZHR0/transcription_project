import os
import re
from datetime import date, datetime
from typing import Tuple

try:
    from subjects import schedule
except ModuleNotFoundError:
    schedule = {}


def clear_terminal() -> None:
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_week_day_and_time(audio_name: str) -> Tuple[str, datetime.time]:
    """
    Returns the day of the week starting from 0 (Monday) and the time of the class from the given audio file name.

    Args:
        audio_name (str): name of the audio file with the pattern: "YYYY-MM-DD HH-MM"

    Returns:
        A tuple containing:
            subject_week_day (str): day of the week starting from 0 (Monday)
            subject_time (datetime.time): time of the class
    """
    pattern = r"\d{4}-\d{2}-\d{2} \d{2}-\d{2}"
    match = re.search(pattern, audio_name)
    date_and_time = datetime.strptime(match.group(), '%Y-%m-%d %H-%M')
    subject_week_day = date.strftime(date_and_time, '%A')
    subject_time = date_and_time.time()
    return subject_week_day, subject_time


def string_to_time(string: str) -> datetime.time:
    """
    Returns a time object from a string with the format "HH:MM".

    Args:
        string (str): string with the time using the pattern: "HH:MM"

    Returns:
        datetime.time: time object
    """
    return datetime.strptime(string, '%H:%M').time()


def get_right_path(main_path: str, s_week_day: str, s_time: str) -> str:
    """
    Returns the right path to the audio file based on the schedule.

    Args:
        main_path (str): path to the folder where the audio file is
        s_week_day (str): week day of the subject
        s_time (str): time of the subject

    Returns:
        str: path to the folder where the audio file should be, otherwise returns the main_path
    """
    for day in schedule:
        if day == s_week_day:
            for subject in schedule[day]:
                if string_to_time(subject['start_time']) <= s_time <= string_to_time(subject['end_time']):
                    return f"{main_path}/{subject['name']}"
    return main_path


def remove_file(file_path: str, file_name: str, ext: str) -> None:
    """
    Removes file from the given path.

    Args:
        file_path (str): path to the file
        file_name (str): name of the file without the extension
        ext (str): extension of the file without the dot
    """
    print(f"""Removing "{file_name}.{ext}"...""")
    os.remove(f"{file_path}/{file_name}.{ext}")
    print(f""""{file_name}.{ext}" was removed!""")


def organize(path: str, file_name: str) -> None:
    """
    Organizes the audio file in the right folder based on the schedule.

    Args:
        path (str): path to the folder where the audio file is
        file_name (str): name of the audio file
    """
    subject_week_day, subject_time = get_week_day_and_time(file_name)
    subject_full_path = get_right_path(path, subject_week_day, subject_time)
    if subject_full_path != path:
        print(f""""{file_name}" is being organized...""")
        try:
            os.rename(f"{path}/{file_name}",
                      f"{subject_full_path}/{file_name}")
        except FileNotFoundError:
            print(f""""{subject_full_path}" does not exist. Creating folder...""")
            os.mkdir(subject_full_path)
            os.rename(f"{path}/{file_name}",
                      f"{subject_full_path}/{file_name}")
        finally:
            print(
                f""""{file_name}" was organized! and moved to {subject_full_path}/{file_name}""")
    else:
        print(
            f""""{file_name}" was not organized because it is not in the schedule.""")
