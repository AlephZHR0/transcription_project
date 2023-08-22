import os
import whisper

model = whisper.load_model('medium')


def get_names(full_path):
    """Returns file_path, file name and extension"""
    file_path = full_path[:full_path.rindex('/')]
    file_name = full_path[full_path.rindex('/') + 1:full_path.rindex('.')]
    ext = full_path[full_path.rindex('.') + 1:]
    return file_path, file_name, ext


def transcribe(file_path, file_name, ext):
    """Transcribes audio file and returns the transcription"""
    print(f""""{file_name}.{ext}" is being transcribed...""")
    audio = whisper.load_audio(f"{file_path}/{file_name}.{ext}")
    transcription = model.transcribe(audio)
    print(f""""{file_name}.{ext}" was successfully transcribed!""")
    return transcription["text"]


def write_txt_file_with_transcription(file_path, file_name, transcription):
    """Writes transcription to a file"""
    print("Creating a file with transcription...")
    with open(f"{file_path}/{file_name}.txt", "w") as f:
        f.write(transcription)
    print(f""""{file_name}.txt" was created with transcription!""")
    return True


def remove_file(file_path, file_name, ext):
    """Removes file from the path"""
    print(f"Removing {file_name}.{ext}...")
    os.remove(f"{file_path}/{file_name}.{ext}")
    print(f"{file_name}.{ext} was removed!")


def transcribe_write_delete(full_path, remove_f=False):
    """Transcribes, writes transcription to a file and removes the file"""
    file_path, file_name, ext = get_names(full_path)
    transcription = transcribe(file_path, file_name, ext)
    write_txt_file_with_transcription(file_path, file_name, transcription)
    if remove_f:
        remove_file(file_path, file_name, ext)
