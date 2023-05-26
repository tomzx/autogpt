from autogpt.middlewares.next_requests import NextRequests
from autogpt.middlewares.request import Request
from autogpt.tasks.base import Task, TaskResponse
from autogpt.utils.lists import extract_list


class Programmer(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Prompt: {query}
        List of steps in YAML format, no prefix/suffix content.
        Format:
        - description: str (the description of the task)
          verbs: python List[str] (the verbs part of the description)
          role: str (the type of role that can complete the task)
          budget: (float, float) (the estimated minimum/maximum budget for the task, in USD $)
          budget_why: str (the reason why the budget is what it is)
          effort: python timedelta (the estimated effort required to complete the task)
          effort_why: str (the reason why the effort is what it is)
          code: Optional[str] (the python code that can complete the task, if applicable)
        """
        # List of steps in YAML format, no prefix/suffix content.
        # Limit to 10 steps.
        # Indicate before each steps in bracket the complexity (low/medium/high), the effort in days, and the expected value generated in dollars.
        # Ask questions when the request is unclear, prefixing them with [q].
        # Return your answer as a python program.
        # Limit to 3 steps.
        # Format:
        # - description: str
        #   verbs: List[str]
        #   budget: float ($)s
        #   effort: timedelta
        #   code: Optional[str]
        # Return each step as a description of the task, an estimated necessary budget,
        # a deadline (now is {datetime.now().isoformat(timespec="minutes")}), and python code if the task
        # can be expressed as such. Return code: null if the task cannot be expressed as code.
        # Return a numerical priority value
        # Identify dependencies between steps
        # return f"""
        # Act as a python programmer.
        # {query}
        # Reply in the format of a python program.
        # You do not have to implement the functions yet, we will do this iteratively.
        # """

    def process_response(self, response: str) -> TaskResponse:
        # TODO(tom@tomrochette.com): Extract the steps from the response
        # and determine the next actions to take.

        items = extract_list(response)
        next_requests = NextRequests()
        for item in items:
            next_requests.add(Request(item, "simple"))
        # TODO(tom@tomrochette.com): Create a prompt from the statements

        return TaskResponse(next_requests)

        #
        # code, language = extract_code(response)
        # if language != "python":
        #     raise ValueError("Response does not contain Python code.")
        #
        # return TaskResponse(NextRequests())
