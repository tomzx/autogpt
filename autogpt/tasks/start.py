from datetime import datetime

from autogpt.tasks.base import Task, TaskResponse
from autogpt.utils.lists import extract_list


class Start(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Prompt: {query}
        Expected output:
        List of steps in YAML format, no prefix/suffix content.
        Limit to 10 steps.
        """
        # Indicate before each steps in bracket the complexity (low/medium/high), the effort in days, and the expected value generated in dollars.
        # Ask questions when the request is unclear, prefixing them with [q].
        # Limit to 3 steps.
        # Format:
        # - description: str
        #   verbs: List[str]
        #   budget: float ($)
        #   effort: timedelta
        #   code: Optional[str]
        # Return each step as a description of the task, an estimated necessary budget,
        # a deadline (now is {datetime.now().isoformat(timespec="minutes")}), and python code if the task
        # can be expressed as such. Return code: null if the task cannot be expressed as code.
        # Return a numerical priority value
        # Identify dependencies between steps

    def process_response(self, response: str) -> TaskResponse:
        # TODO(tom@tomrochette.com): Extract the steps from the response
        # and determine the next actions to take.

        next_queries = extract_list(response)
        # TODO(tom@tomrochette.com): Create a prompt from the statements

        return TaskResponse(next_queries=next_queries)
