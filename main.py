from downloads import download_youtube_audio
from organize import clear_terminal
from subjects_manipulation import (create_subject, remove_subject,
                                   show_all_subjects_by_weekday)
from transcribe import (get_right_model, transcribe_all_files_and_organize,
                        transcribe_all_files_in_a_directory,
                        transcribe_write_delete)
from verifyers import go_to_valid_dir, want_to_remove_file

try:
    model = get_right_model(failed_to_load_sys_info=False)
except Exception:
    print("""There was an error loading the system information, you can continue with the model of your preference, but 
          verify if you have enough memory on your graphics card for the model of your choice.""")
    model = get_right_model(failed_to_load_sys_info=True)
clear_terminal()
while True:
    user_input = input("""1. To see all subjects by weekday
2. Add a subject
3. Remove a subject
4. Transcribe all files in a directory and organize by schedule (locally)
5. Transcribe all files in a directory and don't organize by schedule (locally)
6. Transcribe from a video (online)
'.' To Exit the program at any time
Type your option: """).strip()
    match user_input:
        case "1":
            clear_terminal()
            show_all_subjects_by_weekday()
        case "2":
            clear_terminal()
            create_subject()
        case "3":
            clear_terminal()
            remove_subject()
        case "4":
            clear_terminal()
            remove = want_to_remove_file()
            if remove is None:
                continue
            transcribe_all_files_and_organize(model=model, remove_f=remove)
        case "5":
            clear_terminal()
            remove = want_to_remove_file()
            if remove is None:
                continue
            transcribe_all_files_in_a_directory(model=model, remove_f=remove)
        case "6":
            clear_terminal()
            remove = want_to_remove_file()
            if remove is None:
                continue
            if go_to_valid_dir() is not None:
                transcribe_write_delete(model=model, full_path=download_youtube_audio(
                    input("Type the url of the video: ").strip()), remove_f=remove)
        case ".":
            clear_terminal()
            print("The program ended with no problems")
            exit()
        case _:
            clear_terminal()
            print("Invalid option")
