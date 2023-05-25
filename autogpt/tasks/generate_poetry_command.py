import structlog

from autogpt.tasks.base import Task, TaskResponse
from autogpt.tasks.next_requests import NextRequests

logger = structlog.get_logger(__name__)


class GeneratePoetryCommand(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Generate a list of poetry add commands to install the necessary python libraries for the following imports to work:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        if "```" not in response:
            raise ValueError("Response does not contain code.")

        code = response.split("```")[1].split("```")[0].strip()

        for line in code.splitlines():
            if not line.startswith("poetry"):
                logger.warning("Line does not start with poetry, skipping", line=line)

        # TODO(tom@tomrochette.com): Execute commands in container
        return TaskResponse(NextRequests())
