import structlog

from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse

logger = structlog.get_logger(__name__)


class ReviewCodebase(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse(NextRequests())
