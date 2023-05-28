from typing import Callable

import structlog

from autogpt.backends.base import LLMBase
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.next_requests import NextRequests
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.tasks import all_tasks

logger = structlog.get_logger(__name__)


class CallLLM(Middleware):
    def __init__(self, backend: LLMBase) -> None:
        self.backend = backend

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        if request.task in all_tasks:
            task = all_tasks[request.task](request)
        else:
            raise ValueError(f"Unknown task: {request.task}")

        query = task.prompt(request.prompt)
        logger.debug(f"Generated query", query=query)

        response = Response("", NextRequests(), 0)
        if query != "":
            llm_response = self.backend.query(query)
            response.response = llm_response.response
            response.cost = llm_response.cost
        response.next_requests = task.process_response(response.response).next_requests

        return response
