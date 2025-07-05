from typing import Optional
from autogpt.middlewares.request import Request


class NotionTask:
    def __init__(self, request: Request, budget: float, task_id: str, time_budget: Optional[int] = None) -> None:
        self.request = request
        self.budget = budget
        self.task_id = task_id
        self.time_budget = time_budget
