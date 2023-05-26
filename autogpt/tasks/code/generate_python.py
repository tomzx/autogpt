from autogpt.commands.filesytem.write_file import WriteFile
from autogpt.commands.run_in_container import StartContainer
from autogpt.middlewares.next_requests import NextRequests
from autogpt.tasks.base import Task, TaskResponse
from autogpt.utils.response_helper import extract_code
from autogpt.workspace.workspace import Workspace


class GeneratePython(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Generate python code for the following task:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        code, language = extract_code(response)
        if language != "python":
            raise ValueError("Response does not contain Python code.")

        workspace = Workspace().create()
        file = workspace / "main.py"

        WriteFile(file, code)()

        StartContainer("python:latest", f"python /app/main.py", [f"{workspace}:/app"])()

        # TODO(tom@tomrochette.com): Determine what to do given the script has executed
        return TaskResponse(NextRequests())
