"""A task manager that allows user to schedule and remove tasks when done.

n - create a new task (title, due date(ddmmyyyy), 
optional: schedule(interval(days after next)), subject)
r - remove task (index)
string - sort tasks(key = (subject, due date, alphabetical order))
q - quit app

created by Jack Wong
2023-05-02
"""
import datetime
import os
import sys
from win10toast import ToastNotifier


import task


def load_tasks(lst, file):
    """Load tasks and add them to lst by reading from file."""
    with open(file, "r") as f:
        text = [i.split(", ") for i in f.read().split("\n")]
        text.pop()
    if len(text) > 0:
        for i in text:
            i[1] = datetime.datetime.strptime(i[1], "%Y-%m-%d").date()
            i[2] = datetime.datetime.strptime(i[2], "%Y-%m-%d").date()
            i = [None if j == "None" else j for j in i]
            lst = create_task(lst, i)

    return lst


def write_tasks(lst, file):
    """Write tasks in lst to file
    format: title, due date, schedule, subject"""
    string = ""
    for i in lst:
        string += (
            f"{i.title}, {i.due_date}, {i.created_date}, {i.schedule}, {i.subject}\n"
        )

    with open(file, "w") as f:
        f.write(string)


def check_schedules(lst, schedules):
    """Automatically checks if any schedules are due"""
    added_tasks = []
    for i in schedules:
        if i.schedule is not None:
            if (
                i.created_date + datetime.timedelta(days=+i.schedule)
                == datetime.date.today()
            ):
                create_task(
                    added_tasks,
                    [
                        i.title,
                        i.due_date + datetime.timedelta(days=+int(i.schedule)),
                        datetime.date.today(),
                        i.schedule,
                        i.subject,
                    ],
                )
    lst.extend(added_tasks)
    return lst


def display_notifications(lst, time_delta: int):
    """Creates notifications for task due in time_delta days

    Args:
        lst (list): the list of tasks
        time_delta (int): how many days due tasks to be notified
    """
    for i in lst:
        if i.due_date <= datetime.date.today() + datetime.timedelta(days=+time_delta):
            toaster = ToastNotifier()
            toaster.show_toast(
                f"{i.title}", f"due date: {i.due_date}, subject: {i.subject}"
            )


def display_tasks(lst: list):
    """Prints out all the tasks

    Args:
        tasks (list): contains all object references to the task objects
    """
    for i, value in enumerate(lst):
        print(f"{i+1} - {value}")


def check_date(date):
    """Checks if string is a date

    Args:
        date (_type_): _description_

    Returns:
        bool: true for valid date
    """
    match date.lower():
        case "today":
            date = datetime.date.today()
        case "tomorrow":
            date = datetime.date.today() + datetime.timedelta(day=+1)
        case "next week":
            date = datetime.date.today() + datetime.timedelta(weeks=+1)
        case _:
            pass
    date = list(map(int, date.split("/")))
    flag = True
    if date[1] > 12:
        flag = False
    if (
        date[0] > 31
        or (date[0] > 30 and date[1] in (4, 6, 9, 11))
        or (date[0] > 28 and date[1] == 2)
    ):
        flag = False

    date = datetime.date(year=date[2], month=date[1], day=date[0])
    return flag, date


def create_task(lst: list[task.Task], _details: list):
    """Creates a task"""

    lst.append(task.Task(*_details))
    return lst


def remove_task(lst):
    """Remove task from list

    Args:
        lst (list): contains all tasks to remove
    """
    while True:
        index = input("enter index to remove: ")
        if index == "":
            return lst
        if index.isdigit():
            break
        print("invalid input")
    index = int(index) - 1
    if index < len(lst):
        del lst[index]

    return lst


FILE = "tasks.txt"
SCHEDULE_FILE = "schedule_tasks.txt"
DUE_DATE_DELTA = 3
tasks = []
schedule_tasks = []
tasks = load_tasks(tasks, FILE)
schedule_tasks = load_tasks(schedule_tasks, SCHEDULE_FILE)
tasks = check_schedules(tasks, schedule_tasks)


display_notifications(tasks, DUE_DATE_DELTA)

while True:
    display_tasks(tasks)
    command = input("> ").strip()
    match command:
        case "q":
            write_tasks(tasks, FILE)
            print("exit program")
            sys.exit()
        case "n":
            while True:
                details = input("Create new Task: ").strip().split(", ")
                flag, date = check_date(details[1])
                if flag:
                    break
            details[1] = date
            details.insert(2, datetime.date.today())
            if len(details) > 3:
                if details[3] == "None":
                    details[3] = None
                else:
                    schedule_tasks = create_task(schedule_tasks, details)
            tasks = create_task(tasks, details)
        case "r":
            remove_task(tasks)
        case "rs":
            display_tasks(schedule_tasks)
            remove_task(schedule_tasks)
        case "s":
            write_tasks(tasks, FILE)
            write_tasks(schedule_tasks, SCHEDULE_FILE)
        case _:
            pass
    os.system("cls")
