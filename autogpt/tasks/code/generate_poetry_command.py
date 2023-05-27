import structlog

from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse

logger = structlog.get_logger(__name__)


class GeneratePoetryCommand(Task):
    name = "generate-poetry-command"

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
