from typing import Callable

import structlog

from autogpt.backends.base import LLMBase
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.tasks.next_requests import NextRequests
from autogpt.tasks.query_multiple_personas import QueryMultiplePersonas
from autogpt.tasks.simple import Simple
from autogpt.tasks.summarize import Summarize
from autogpt.tasks.summarize_multiple_personas import SummarizeMultiplePersonas
from autogpt.tasks.summarize_responses import SummarizeResponses

logger = structlog.get_logger(__name__)


class CallLLM(Middleware):
    def __init__(self, backend: LLMBase) -> None:
        self.backend = backend

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        # TODO(tom.rochette@coreteks.org): Generalize task selection process
        # i.e., use a registry + a name attribute to identify the tasks
        task = Simple()
        if request.task == "query-multiple-personas":
            task = QueryMultiplePersonas()
        elif request.task == "summarize-multiple-personas":
            task = SummarizeMultiplePersonas()
        elif request.task == "summarize-responses":
            task = SummarizeResponses(request.needs)
        elif request.task == "summarize":
            task = Summarize()

        query = task.prompt(request.prompt)
        logger.debug(f"Generated query", query=query)

        response = Response("", NextRequests(), 0)
        if query != "":
            llm_response = self.backend.query(query)
            response.response = llm_response.response
            response.cost = llm_response.cost
        response.next_requests = task.process_response(response.response).next_requests

        return response
