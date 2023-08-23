import os
from data import path
from transcribe import transcribe_write_delete, get_names
from organize import organize

accepted_audio_formats = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]

for record in os.listdir(path):
    if os.path.isfile(f"{path}/{record}"):
        _, file_name, file_ext = get_names(f"{path}/{record}")
        if file_ext in accepted_audio_formats:
            pass
            transcribe_write_delete(f"{path}/{record}")
            organize(path, f"{file_name}.txt")
        elif file_ext == "txt":
            organize(path, record)
        else:
            print(f"{record} is not a valid file")
