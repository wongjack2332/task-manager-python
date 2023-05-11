import datetime
import task


def create_task(lst, _details):
    """Creates a task"""

    lst.append(task.Task(*_details))
    return lst


def check_schedules(lst):
    """Automatically checks if any schedules are due"""
    for i in lst:
        if (
            i.created_date + datetime.timedelta(days=+i.schedule)
            == datetime.date.today()
        ):
            create_task(
                tasks,
                [
                    i.title,
                    i.due_date + datetime.timedelta(days=+int(i.schedule)),
                    i.schedule,
                    i.subject,
                ],
            )


tasks = []
tasks = create_task(tasks, ["sparx", datetime.date(2023, 5, 12), "0"])
check_schedules(tasks)
