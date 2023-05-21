import structlog
import tiktoken

from autogpt.backends.openai.message import AssistantMessage
from autogpt.middlewares.request import Request
from autogpt.session.session import Session
from autogpt.tasks.base import Task, TaskResponse

logger = structlog.get_logger(__name__)


class SummarizeResponses(Task):
    def __init__(self, session: Session) -> None:
        super().__init__()
        self.past_response_count = 0
        self.session = session

    def generate_prompt(self, query: str) -> str:
        self.past_response_count = int(query)
        logger.debug(
            "Will summarize past responses",
            past_response_count=self.past_response_count,
        )
        return ""

    def process_response(self, response: str) -> TaskResponse:
        responses = []
        tokens = 0
        for response in reversed(self.session.messages):
            if isinstance(response, AssistantMessage):
                # TODO(tom@tomrochette.com): Get model from somewhere, request maybe?
                tokens += len(
                    tiktoken.encoding_for_model("gpt-3.5-turbo").encode(
                        response.content
                    )
                )
                if tokens > 4000:
                    logger.debug(
                        "Too many tokens to summarize, summary content will be truncated",
                        tokens=tokens,
                        max_tokens=4000,
                        past_response_count=len(responses),
                        max_past_response_count=self.past_response_count,
                    )
                    break

                responses += [response.content]

                if len(responses) >= self.past_response_count:
                    break

        return TaskResponse([Request("\n".join(reversed(responses)), "summarize")])
