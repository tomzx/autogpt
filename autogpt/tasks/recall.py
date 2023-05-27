from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse


class Recall(Task):
    name = "recall"

    def generate_prompt(self, query: str) -> str:
        return f"""
        Prompt: {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
