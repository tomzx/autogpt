from datetime import datetime


class DeadlineBudget:
    def __init__(self) -> None:
        self.deadline = None

    def set_deadline(self, deadline: datetime) -> None:
        self.deadline = deadline

    def is_deadline_reached(self) -> bool:
        if self.deadline is None:
            return False

        return datetime.now() >= self.deadline
