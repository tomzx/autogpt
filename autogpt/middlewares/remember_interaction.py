from typing import Callable
from uuid import uuid4

from autogpt.backends.openai.message import AssistantMessage, Message, UserMessage
from autogpt.memory.base import Memory
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.session.session import Session


class RememberInteraction(Middleware):
    def __init__(self, memory: Memory, session: Session) -> None:
        self.memory = memory
        self.session = session

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        response = next(request)

        # self.memory.update(uuid4(), Interaction()
        self.session.add_message(UserMessage(request.prompt))
        self.session.add_message(AssistantMessage(response.response))

        return response
