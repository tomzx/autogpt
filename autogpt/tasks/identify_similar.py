from autogpt.tasks.base import Task, TaskResponse


class IdentifySimilar(Task):
    def generate_prompt(self, query: str) -> str:
        return f"""
        Are there similar tasks in the following list? If so, indicate the task numbers and indicate why.
        {query}
        """

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse([])
