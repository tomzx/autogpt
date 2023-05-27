from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse


class SummarizeCodeChanges(Task):
    name = "summarize-code-changes"

    def generate_prompt(self, query: str) -> str:
        return f"""
        Summarize code changes based on the following diff:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
