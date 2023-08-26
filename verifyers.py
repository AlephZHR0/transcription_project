import os
from organize import get_week_day_and_time, get_right_path

def is_already_transcribed(path: str, file_name: str) -> bool:
    existent_subjects = []
    for dir in os.listdir(path):
        if os.path.isdir(f"{path}/{dir}"):
            existent_subjects.append(dir)
    subject_week_day, subject_time = get_week_day_and_time(f"{path}/{file_name}.txt")
    subject_path = get_right_path(path, subject_week_day, subject_time)
    if f"{file_name}.txt" in os.listdir(subject_path):
        return True
    else:
        return False
