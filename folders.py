import os

def create_folders_for_subjects(path: str, schedule: dict) -> None:
    """Creates folders for each subject"""
    subjects = [subject['name'] for day in schedule for subject in schedule[day]]
    for day in schedule:
        for subject in schedule[day]:    
            if not os.path.exists(f"{path}/{subject['name']}"):
                os.mkdir(f"{path}/{subject['name']}")
