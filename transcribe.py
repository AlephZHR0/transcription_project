import os
from typing import Tuple
from organize import get_week_day_and_time
from datetime import datetime
try:
    from subjects import schedule
except ModuleNotFoundError:
    schedule = {}
import whisper

from get_pc_specs import get_specs_and_return_right_model
from organize import organize, remove_file
from verifyers import go_to_valid_dir, is_already_transcribed
from pydub import AudioSegment

ACCEPTED_AUDIO_FORMATS = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]
MODELS = ["tiny", "base", "small", "medium", "large-v3"]


def trim_audio_file_into_class_time(file_path: str, file_name: str, ext: str) -> None:
    """
    Trims audio file into class time
    
    Args:
        file_path (str): Path to the file
        file_name (str): Name of the file without the extension
        ext (str): Extension of the file without the dot
    """
    def class_time_to_miliseconds(class_time: datetime.time) -> int:
        return (class_time.seconds) + ((class_time.minutes + 5) * 60) + (class_time.hours * 3600)
    

    subject_week_day, subject_time = get_week_day_and_time(f"{file_path}/{file_name}.{ext}")
    for subject in schedule[subject_week_day]:
        if subject["start_time"] <= subject_time <= subject["end_time"]:
            class_time = subject["end_time"] - subject["start_time"]
            break
    
    print(f""""{file_name}.{ext}" is being trimmed into class time...""")
    song = AudioSegment.from_file(f"{file_path}/{file_name}/{ext}", format=f"{ext}")
    class_to_the_end = song[:class_time_to_miliseconds(class_time)]
    class_to_the_end.export(f"{file_path}/{file_name}.{ext}", format=f"{ext}")
    print("New Audio file is created and saved")
    print(f""""{file_name}.{ext}" was successfully trimmed into class time!""")


# TODO make a function that sees the audio duration and check if it recorded the next class, if true, trim 5 min before and 5 the duration of next class + 5 min
# TODO: combine the two functions above into one
# TODO: run it before the transcribe_all_files_and_organize on main.py to certify that the audio file is trimmed into class time and got all the classes recorded even when forget to stop the recording


def get_right_model(failed_to_load_sys_info: bool = False) -> whisper.model:
    """
    Returns the right model based on the available memory

    Args:
        failed_to_load_sys_info (bool): If True, returns the first model

    Returns:
        whisper.model: The selected model
    """
    if not failed_to_load_sys_info:
        recomended_model, available_memory = get_specs_and_return_right_model()
    else:
        recomended_model = MODELS[0]
        available_memory = "N/A"
    user_model_of_choice = input(f"""The available models are:
1. {MODELS[0]}
2. {MODELS[1]}
3. {MODELS[2]}
4. {MODELS[3]}
5. {MODELS[4]}
The recommended model for your computer is {recomended_model} because you have {available_memory} Mib. Press enter to continue with the recomended model, or select the number for using the model of your choice: """)
    if user_model_of_choice == ".": exit()
    else:
        match user_model_of_choice:
            case ".": exit()
            case "5": model = whisper.load_model(MODELS[4])
            case "4": model = whisper.load_model(MODELS[3])
            case "3": model = whisper.load_model(MODELS[2])
            case "2": model = whisper.load_model(MODELS[1])
            case "1": model = whisper.load_model(MODELS[0])
            case _:
                print(
                    f"Using {recomended_model} model because you didn't type anything, or you typed an invalid number")
                model = MODELS[0]
    return model


def get_names(full_path: str) -> Tuple[str, str, str]:
    """
    Returns file_path, file_name and extension

    Args:
        full_path (str): Full path to the file

    Returns:
        A tuple containing:
            file_path (str): Path to the file
            file_name (str): Name of the file without the extension
            ext (str): Extension of the file without the dot
    """
    file_path, file_name_ext = os.path.split(full_path)
    file_name, ext = os.path.splitext(file_name_ext)
    return file_path, file_name, ext[1:]


def transcribe(model:whisper.model, file_path: str, file_name: str, ext: str) -> str:
    """
    Transcribes audio file and returns the transcription

    Args:
        model (whisper.model): Model to be used for transcribing
        file_path (str): Path to the file
        file_name (str): Name of the file without the extension
        ext (str): Extension of the file without the dot

    Returns:
        str: Transcription of the audio file
    """
    print(f""""{file_name}.{ext}" is being transcribed...""")
    audio = whisper.load_audio(f"{file_path}/{file_name}.{ext}")
    transcription = model.transcribe(audio)
    print(f""""{file_name}.{ext}" was successfully transcribed!""")
    return transcription["text"]


def write_txt_file_with_transcription(file_path: str, file_name: str, transcription: str) -> None:
    """
    Writes transcription to a file

    Args:
        file_path (str): Path to the file
        file_name (str): Name of the file without the extension
        transcription (str): Transcription of the audio file
    """
    print("Creating a file with transcription...")
    with open(f"{file_path}/{file_name}.txt", "w", encoding='utf-8') as f:
        f.write(transcription)
    print(f""""{file_name}.txt" was created with transcription!""")


def transcribe_write_delete(model: whisper.model, full_path: str, remove_f: bool = False) -> None:
    """
    Transcribes, writes transcription to a file and removes the file

    Args:
        model (whisper.model): Model to be used for transcribing
        full_path (str): Full path to the file
        remove_f (bool): If True, removes the file after transcribing
    """
    file_path, file_name, ext = get_names(full_path)
    transcription = transcribe(model, file_path, file_name, ext)
    write_txt_file_with_transcription(file_path, file_name, transcription)
    if remove_f:
        remove_file(file_path, file_name, ext)


def transcribe_all_files_in_a_directory(model: whisper.model, remove_f: bool = False) -> None:
    """
    Transcribes all files in a directory

    Args:
        model (whisper.model): Model to be used for transcribing
    """
    go_to_valid_dir()
    path = os.getcwd()
    for record in os.listdir(path):
        record_path = f"{path}/{record}"
        if os.path.isfile(record_path):
            _, _, file_ext = get_names(record_path)
            if file_ext in ACCEPTED_AUDIO_FORMATS:
                transcribe_write_delete(model, record_path, remove_f=remove_f)
            else:
                print(f"{record} is not a valid file")
        else:
            print(f"{record} is not a file")


def transcribe_all_files_and_organize(model: whisper.model,remove_f: bool = False) -> None:
    """
    Transcribes all files in a directory and organizes them in subjects based on your schedule

    Args:
        model (whisper.model): Model to be used for transcribing
        remove_f (bool): If True, removes the file after transcribing
    """
    user_input = input(
        "Do you want to transcribe all files in a directory and organize by schedule? (y/n): ").strip().lower()
    if user_input == "y":
        path = input("Type the path to the directory: ").strip()
        if not os.path.exists(path):
            print(f"{path} does not exist")
            return
        if not os.path.isdir(path):
            print(f"{path} is not a directory")
            return
    elif user_input == "n":
        return
    elif user_input == ".":
        exit()
    for record in os.listdir(path):
        record_path = f"{path}/{record}"
        if os.path.isfile(record_path):
            file_path, file_name, file_ext = get_names(record_path)
            if file_ext in ACCEPTED_AUDIO_FORMATS:
                if not is_already_transcribed(file_path, file_name):
                    transcribe_write_delete(model, record_path, remove_f=remove_f)
                    organize(file_path, f"{file_name}.txt")
                else:
                    print(f"{record} is already transcribed")
                    if remove_f:
                        remove_file(file_path, file_name, file_ext)
            elif file_ext == "txt":
                organize(file_path, record)
            else:
                print(f"{record} is not a valid file")