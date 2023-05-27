from autogpt.middlewares.next_requests import NextRequests
from autogpt.middlewares.request import Request
from autogpt.tasks.base import TaskResponse
from autogpt.tasks.text.query_multiple_personas import QueryMultiplePersonas
from autogpt.tasks.text.select_personas import personas


class SummarizeMultiplePersonas(QueryMultiplePersonas):
    name = "summarize-multiple-personas"

    def process_response(self, response: str) -> TaskResponse:
        next_requests = NextRequests()
        needs = []
        for persona in personas:
            needs += [next_requests.add(Request(persona["prompt"] + "\n" + self.query, "simple"))]
        next_requests.add(Request("", "summarize-responses"), needs)
        return TaskResponse(next_requests)
