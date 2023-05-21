from autogpt.middlewares.request import Request
from autogpt.tasks.base import TaskResponse
from autogpt.tasks.query_multiple_personas import QueryMultiplePersonas


class SummarizeMultiplePersonas(QueryMultiplePersonas):
    def process_response(self, response: str) -> TaskResponse:
        next_requests = []
        for persona in self.personas:
            next_requests += [Request(persona["prompt"] + "\n" + self.query, "simple")]
        next_requests += [Request(str(len(next_requests)), "summarize-responses")]
        return TaskResponse(next_requests)
