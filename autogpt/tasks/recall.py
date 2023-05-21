from autogpt.tasks.base import Task, TaskResponse


class Remember(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Prompt: {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse([])
