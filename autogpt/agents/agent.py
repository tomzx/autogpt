import asyncio
import os
from collections import deque
from typing import List, Optional

import structlog
from dask import compute, delayed
from dotenv import load_dotenv
from tortoise import Tortoise

from autogpt.backends.debug.debug import Debug
from autogpt.backends.openai.api import Api
from autogpt.budget.money_budget import MoneyBudget
from autogpt.memory.ram import RAM
from autogpt.middlewares.call_llm import CallLLM
from autogpt.middlewares.execute import call
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.profiler import Profiler
from autogpt.middlewares.remember_interaction import RememberInteraction
from autogpt.middlewares.request import Request
from autogpt.middlewares.save_to_database import SaveToDatabase
from autogpt.middlewares.save_to_notion import SaveToNotion
from autogpt.notion.notion import Notion
from autogpt.session.session import Session

logger = structlog.get_logger(__name__)


class Agent:
    """
    An agent is responsible for working toward a goal.
    To do so, it will call a LLM to determine what to do, then will execute
    the necessary action within its environment.
    """

    def __init__(self) -> None:
        self.money_budget = MoneyBudget()
        self.session = Session()

    def initialize(self) -> None:
        load_dotenv(override=True)
        asyncio.run(self.initialize_database())

    async def initialize_database(self) -> None:
        # TODO(tom@tomrochette.com): Plan for per agent database
        await Tortoise.init(
            db_url="sqlite://db.sqlite3",
            modules={"models": ["autogpt.models"]},
        )
        await Tortoise.generate_schemas()

    def get_middleware(self) -> List[Middleware]:
        middlewares = [
            # CallLLM(Debug()),
            CallLLM(Api(os.environ.get("OPENAI_API_KEY"))),
            RememberInteraction(RAM(), self.session),
            SaveToNotion(Notion(), self.money_budget),
            SaveToDatabase(self.session.model()),
        ]

        if os.environ.get("DEBUG") == "1":
            for index, middleware in enumerate(middlewares):
                middlewares[index] = Profiler(middleware)

        # TODO(tom@tomrochette.com): Make this configurable outside of this file
        return middlewares

    def execute(
        self,
        request: str,
        budget: Optional[float] = None,
        notion_interaction_id: Optional[str] = None,
    ) -> None:
        self.initialize()
        self.session.start()
        self.money_budget.set_budget(budget)

        middlewares = self.get_middleware()

        initial_request = Request(request)
        initial_request.notion_interaction_id = notion_interaction_id
        # TODO(tom@tomrochette.com): Replace with a priority
        queries = deque([initial_request])
        while True:
            if not queries:
                logger.debug("No more queries to process")
                break

            if self.should_terminate():
                logger.debug("Budget exhausted")
                break

            request = queries.popleft()
            response = call(middlewares, request)
            logger.debug("Response", response=response.response)

            queries.extend(response.next_queries)
            # computation = []
            # for next_query in response.next_queries:
            #     computation += [execute(next_query.prompt, self.money_budget.budget, next_query.notion_interaction_id)]
            #
            # compute(*computation)

            self.money_budget.update_spent_budget(response.cost)

            # TODO(tom@tomrochette.com): Determine when it can delegate to other agents

        self.session.end()

    def should_terminate(self) -> bool:
        return self.money_budget.is_budget_reached()


def execute(
    query: str, budget: Optional[float], notion_interaction_id: Optional[str] = None
) -> None:
    Agent().execute(query, budget, notion_interaction_id)
