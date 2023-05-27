from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse


class Summarize(Task):
    name = "summarize"

    def generate_prompt(self, query: str) -> str:
        return f"""
        Summarize the following text as a list of bullet points:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
