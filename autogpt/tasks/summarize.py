from autogpt.tasks.base import Task, TaskResponse


class Summarize(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Summarize the following text:
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse([])
