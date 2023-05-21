from autogpt.tasks.base import Task, TaskResponse


class Simple(Task):
    def generate_prompt(self, query: str) -> str:
        return query

    def process_response(self, response: str) -> TaskResponse:
        return TaskResponse([])
