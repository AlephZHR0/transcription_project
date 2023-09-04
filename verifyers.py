import os

from organize import get_right_path, get_week_day_and_time


def want_to_remove_file() -> bool:
    """
    returns True if the user wants to remove the file after transcribing, False otherwise.
    """
    remove_file = input(
        "Do you want to remove the files after transcribing? (y/n): ").strip().lower()
    if remove_file == "y":
        return True
    elif remove_file == "n":
        return False
    elif remove_file == ".":
        exit()
    else:
        print("Invalid option. Please try again")
        return None


def is_already_transcribed(path: str, file_name: str) -> bool:
    """
    Verifies if the audio file is already transcribed by checking if a corresponding .txt file exists in the correct folder.

    Args:
        path (str): The path to the folder where the audio file is located.
        file_name (str): The name of the audio file.

    Returns:
        bool: True if the file is already transcribed, False otherwise.
    """
    subject_week_day, subject_time = get_week_day_and_time(
        f"{path}/{file_name}.txt")
    subject_path = get_right_path(path, subject_week_day, subject_time)
    try:
        if f"{file_name}.txt" in os.listdir(subject_path):
            return True
        else:
            return False
    except:
        return False


def go_to_valid_dir():
    path = input("""Please enter a directory path
If you want to use the current directory, just press enter
To exit, type "." and press enter: """).strip()
    match path:
        case "":
            os.chdir(os.getcwd())
            return os.getcwd()
        case ".":
            exit()
        case _ if os.path.isdir(path):
            os.chdir(path)
            return os.getcwd()
        case _:
            print("Invalid directory path. Please try again.")
            return None
