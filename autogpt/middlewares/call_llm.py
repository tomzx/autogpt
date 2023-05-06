import os
from typing import Callable

import structlog

from autogpt.backends.base import LLMBase
from autogpt.backends.openai.api import Api
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.tasks.start import Start

logger = structlog.get_logger(__name__)


class CallLLM(Middleware):
    def __init__(self, backend: LLMBase) -> None:
        self.backend = backend

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        # TODO(tom.rochette@coreteks.org): Decide which task to execute
        task = Start()
        query = task.prompt(request.prompt)
        logger.debug(f"Generated query", query=query)

        response = self.backend.query(query)
        next_queries = task.process_response(response.response).next_queries
        next_queries = [Request(next_query) for next_query in next_queries]

        return Response(response.response, next_queries, response.cost)
