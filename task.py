
class Task:
    """Task with title, due date schedule and subject."""

    def __init__(self, title, due_date, created_date, schedule=None, subject=None):
        self.title = title
        self.due_date = due_date
        if schedule is None:
            self.schedule = None
        else:
            self.schedule = int(schedule)
        self.subject = subject

        self.created_date = created_date

    def __repr__(self) -> str:
        return f"{self.title} : {self.due_date}    schd : {self.schedule}  sub : {self.subject}"
