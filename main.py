import os
from data import path
from transcribe import transcribe_write_delete, get_names
from organize import organize, remove_file
from verifyers import is_already_transcribed

accepted_audio_formats = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

for record in os.listdir(path):
    if os.path.isfile(f"{path}/{record}"):
        _, file_name, file_ext = get_names(f"{path}/{record}")
        if file_ext in accepted_audio_formats:
            if not is_already_transcribed(path, file_name):    
                transcribe_write_delete(f"{path}/{record}")
                organize(path, f"{file_name}.txt")
            else:
                print(f"{record} is already transcribed")
                remove_file(path, file_name, file_ext)
        elif file_ext == "txt":
            organize(path, record)
        else:
            print(f"{record} is not a valid file")
print("The program ended with no problems")