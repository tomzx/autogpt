from autogpt.tasks.base import Task, TaskResponse
from autogpt.tasks.next_requests import NextRequests


class ReviewTasks(Task):
    """
    Review the tasks estimated effort, value, and deadline.
    """

    def generate_prompt(self, query: str) -> str:
        return f"""
        Prompt: {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
