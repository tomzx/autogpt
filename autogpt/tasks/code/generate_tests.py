from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse


class GenerateTests(Task):
    name = "generate-tests"

    def generate_prompt(self, query: str) -> str:
        return f"""
        Generate tests for the following code:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
