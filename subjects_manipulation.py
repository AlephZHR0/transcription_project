from typing import Dict, Tuple

from messages import help_message_subjects_example
from organize import clear_terminal, string_to_time

try:
    from subjects import schedule
except ImportError:
    schedule = {}

week_days = ["Monday", "Tuesday", "Wednesday",
             "Thursday", "Friday", "Saturday", "Sunday"]


def write_schedule_to_file(schedule: Dict[str, list]) -> None:
    """
    Writes the schedule to a file.

    Args:
        schedule (dict): A dictionary containing the schedule.
    """
    with open("subjects.py", "w", encoding='utf-8') as f:
        f.write(f"schedule = {schedule}")


def get_subject_info() -> Tuple[str, str, str, str] or Tuple[None, None, None, None]:
    """
    Prompts the user to enter subject information and returns it.

    Returns:
        tuple: A tuple containing the following strings:
            subject_week_day: The week day of the subject.
            subject_name: The name of the subject.
            subject_start_time: The start time of the subject.
            subject_end_time: The end time of the subject.
    """
    subject_week_day = input(f"""Choose a day using the numbers: 
1 - {week_days[0]}
2 - {week_days[1]}
3 - {week_days[2]}
4 - {week_days[3]}
5 - {week_days[4]}
6 - {week_days[5]}
7 - {week_days[6]}
Choice: """.strip())
    if subject_week_day == ".":
        exit()
    elif subject_week_day not in "1234567":
        print("Invalid input")
        return None, None, None, None
    else:
        subject_week_day = int(subject_week_day)
    subject_week_day = week_days[subject_week_day - 1]
    exit() if (subject_name := input("Subject name: ").strip().capitalize()) == "." else None
    exit() if (subject_start_time := input("Start time: ").strip()) == "." else None
    try:
        string_to_time(subject_start_time)
    except ValueError:
        clear_terminal()
        print("Invalid starting time, try again with the format HH:MM")
        return subject_week_day, subject_name, None, None
    exit() if (subject_end_time := input("End time: ").strip()) == "." else None
    try:
        string_to_time(subject_end_time)
    except ValueError:
        clear_terminal()
        print("Invalid ending time, try again with the format HH:MM")
        return subject_week_day, subject_name, subject_start_time, None
    return subject_week_day, subject_name, subject_start_time, subject_end_time


def create_week_day_in_schedule(week_day_index: int) -> None:
    """
    Creates a new week day in the schedule.

    Args:
        week_day_index (int): The index of the week day.
    """
    week_day = week_days[week_day_index]
    schedule[week_day] = []
    write_schedule_to_file(schedule)


def show_all_subjects_by_weekday() -> None:
    """ 
    Displays all subjects by weekday.
    """
    for week_day in schedule:
        week_day_index = week_days.index(week_day) + 1
        print(f"{week_day_index}. {week_day}:")
        counter = 1
        for subject in schedule[week_day]:
            print(
                f"{week_day_index}.{counter}. {subject['name']}, {subject['start_time']} - {subject['end_time']}")
            counter += 1
        print()


def create_subject() -> None:
    """
    Adds a new subject to the schedule.
    """
    subject_week_day, subject_name, subject_start_time, subject_end_time = get_subject_info()
    details_list = [subject_week_day, subject_name,
                    subject_start_time, subject_end_time]
    if None in details_list:
        print(
            f"""There was an error creating "{subject_name}" and the subject was not added to the schedule. Please 
            try again""")
        return
    try:
        schedule[subject_week_day].append(
            {"name": subject_name, "start_time": subject_start_time, "end_time": subject_end_time})
    except KeyError:
        create_week_day_in_schedule(week_days.index(subject_week_day))
        schedule[subject_week_day].append(
            {"name": subject_name, "start_time": subject_start_time, "end_time": subject_end_time})
    finally:
        schedule[subject_week_day].sort(
            key=lambda x: string_to_time(x["start_time"]))
        write_schedule_to_file(schedule)
    clear_terminal()
    print(f"Subject {subject_name} added successfully")


def remove_subject() -> None:
    """
    Removes a subject from the schedule.
    """
    show_all_subjects_by_weekday()
    user_input = input("""Type the number of the subject you want to remove using the format "weekday.subject_number"
Type 'clear' to remove all subjects
Type '0' to return
If you need help type 'h': """).strip()
    match user_input:
        case "h":
            clear_terminal()
            print(help_message_subjects_example)
        case "clear":
            if input("""Are you sure you want to clear all the subjects?
    Type y to confirm and n to return""") == "y":
                schedule.clear()
            write_schedule_to_file(schedule)
        case "":
            return
        case ".":
            exit()
        case _:
            try:
                week_day_index = int(user_input.split(".")[0]) - 1
                subject_index = int(user_input.split(".")[1]) - 1
                week_day = week_days[week_day_index]
                clear_terminal()
                print(
                    f""""{schedule[week_day].pop(subject_index)["name"]}" was removed!""")
                if schedule[week_day] == []:
                    schedule.pop(week_day)
                    print(f"""There was no subject left in {week_day}
{week_day} was removed!""")
                write_schedule_to_file(schedule)
            except (IndexError, ValueError):
                print("Invalid input")
