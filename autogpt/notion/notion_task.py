from autogpt.middlewares.request import Request


class NotionTask:
    def __init__(self, request: Request, budget: float, task_id: str) -> None:
        self.request = request
        self.budget = budget
        self.task_id = task_id
