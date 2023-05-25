from autogpt.tasks.base import Task, TaskResponse
from autogpt.tasks.next_requests import NextRequests

class Summarize(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Summarize the following text:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
