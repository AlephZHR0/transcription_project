import os
import whisper
from organize import remove_file
model = whisper.load_model('medium')


def get_names(full_path: str) -> tuple:
    """Returns file_path, file name and extension"""
    file_path = full_path[:full_path.rindex('/')]
    file_name = full_path[full_path.rindex('/') + 1:full_path.rindex('.')]
    ext = full_path[full_path.rindex('.') + 1:]
    return file_path, file_name, ext


def transcribe(file_path: str, file_name: str, ext: str) -> str:
    """Transcribes audio file and returns the transcription"""
    print(f""""{file_name}.{ext}" is being transcribed...""")
    audio = whisper.load_audio(f"{file_path}/{file_name}.{ext}")
    transcription = model.transcribe(audio)
    print(f""""{file_name}.{ext}" was successfully transcribed!""")
    return transcription["text"]


def write_txt_file_with_transcription(file_path: str, file_name: str, transcription: str) -> None:
    """Writes transcription to a file"""
    print("Creating a file with transcription...")
    with open(f"{file_path}/{file_name}.txt", "w") as f:
        f.write(transcription)
    print(f""""{file_name}.txt" was created with transcription!""")


def transcribe_write_delete(full_path: str, remove_f: bool = False) -> None:
    """Transcribes, writes transcription to a file and removes the file"""
    file_path, file_name, ext = get_names(full_path)
    transcription = transcribe(file_path, file_name, ext)
    write_txt_file_with_transcription(file_path, file_name, transcription)
    if remove_f:
        remove_file(file_path, file_name, ext)
