from typing import Callable

import structlog

from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.notion.notion import Notion
from autogpt.utils.debug import is_debug

logger = structlog.get_logger(__name__)


class SaveToNotion(Middleware):
    def __init__(self, notion: Notion) -> None:
        self.notion = notion

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        response = next(request)

        if not is_debug() and self.notion.has_api_token():
            interaction = self.notion.create_interaction(
                request.prompt,
                response.response,
                request.task,
                request.notion_session_id,
                request.notion_interaction_id,
                round(response.cost, 6),
            )

            for node in response.next_requests.nodes:
                node.request.notion_session_id = request.notion_session_id
                node.request.notion_interaction_id = interaction["id"]

        return response
