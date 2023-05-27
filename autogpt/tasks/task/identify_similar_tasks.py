from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse


class IdentifySimilarTasks(Task):
    name = "identify-similar-tasks"

    def generate_prompt(self, query: str) -> str:
        return f"""
        Are there similar tasks in the following list? If so, indicate the task numbers and indicate why.
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
