from typing import List

import structlog
import tiktoken

from autogpt.middlewares.next_requests import NextRequests
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.tasks.base import Task, TaskResponse

logger = structlog.get_logger(__name__)


class SummarizeResponses(Task):
    def __init__(self, needs: List[Response]) -> None:
        super().__init__()
        self.needs = needs

    def generate_prompt(self, query: str) -> str:
        return ""

    def process_response(self, response: str) -> TaskResponse:
        responses = []
        tokens = 0
        for response in self.needs:
            # TODO(tom@tomrochette.com): Get model from somewhere, request maybe?
            tokens += len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(response.response))
            if tokens > 4000:
                logger.debug(
                    "Too many tokens to summarize, summary content will be truncated",
                    tokens=tokens,
                    max_tokens=4000,
                    past_response_count=len(responses),
                    max_past_response_count=len(self.needs),
                )
                break

            responses += [response.response]

        next_requests = NextRequests()
        next_requests.add(Request("\n".join(reversed(responses)), "summarize"))
        return TaskResponse(next_requests)
