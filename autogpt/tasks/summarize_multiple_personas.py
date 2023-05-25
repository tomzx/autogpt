from autogpt.middlewares.request import Request
from autogpt.tasks.base import TaskResponse
from autogpt.tasks.next_requests import NextRequests
from autogpt.tasks.query_multiple_personas import QueryMultiplePersonas


class SummarizeMultiplePersonas(QueryMultiplePersonas):
    def process_response(self, response: str) -> TaskResponse:
        next_requests = NextRequests()
        needs = []
        for persona in self.personas:
            needs += [next_requests.add(Request(persona["prompt"] + "\n" + self.query, "simple"))]
        next_requests.add(Request("", "summarize-responses"), needs)
        return TaskResponse(next_requests)
