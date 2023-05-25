import structlog

from autogpt.tasks.base import Task, TaskResponse
from autogpt.tasks.next_requests import NextRequests

logger = structlog.get_logger(__name__)


class ReviewCodebase(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
