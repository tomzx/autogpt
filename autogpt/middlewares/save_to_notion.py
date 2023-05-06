from typing import Callable

import structlog

from autogpt.budget.money_budget import MoneyBudget
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.notion.notion import Notion

logger = structlog.get_logger(__name__)


class SaveToNotion(Middleware):
    def __init__(self, notion: Notion, budget: MoneyBudget) -> None:
        self.notion = notion
        if self.notion.has_api_token():
            self.session = self.notion.create_session(budget.budget)
            logger.debug("Notion session started", session_id=self.session["id"])

    def handle(self, request: Request, next: Callable[[Request], Response]) -> Response:
        response = next(request)

        if self.notion.has_api_token():
            interaction = self.notion.create_interaction(
                request.prompt,
                response.response,
                self.session["id"],
                request.notion_interaction_id,
                response.cost,
            )

            for next_query in response.next_queries:
                next_query.notion_interaction_id = interaction["id"]

        return response
