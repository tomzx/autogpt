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
            # TODO(tom@tomrochette.com): Add a middleware that would prevent the CallLLM
            # middleware from being called if the task does not need to call the LLM.
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
        task: str,
        budget: Optional[float] = None,
        notion_interaction_id: Optional[str] = None,
    ) -> None:
        self.initialize()
        self.session.start()
        self.money_budget.set_budget(budget)

        middlewares = self.get_middleware()

        # TODO(tom@tomrochette.com): We need to know if we're asked to execute
        # a single query or a query that will require a graph to be resolved.
        # In the case of a graph, we will want to execute the nodes that can
        # be executed once their dependencies have been resolved.
        initial_request = Request(request, task)
        initial_request.notion_interaction_id = notion_interaction_id
        # TODO(tom@tomrochette.com): Replace with a priority
        requests = deque([initial_request])
        while True:
            if not requests:
                logger.debug("No more requests to process")
                break

            if self.should_terminate():
                logger.debug("Budget exhausted")
                break

            request = requests.popleft()

            # Set properties on the request
            request.session = self.session

            response = call(middlewares, request)
            logger.debug("Response", response=response.response)

            requests.extend(response.next_requests)
            # computation = []
            # for next_query in response.next_queries:
            #     computation += [execute(next_query.prompt, next_query.task, self.money_budget.budget, next_query.notion_interaction_id)]
            #
            # compute(*computation)

            self.money_budget.update_spent_budget(response.cost)

            # TODO(tom@tomrochette.com): Determine when it can delegate to other agents

        self.session.end()

    def should_terminate(self) -> bool:
        return self.money_budget.is_budget_reached()


def execute(
    query: str,
    task: str,
    budget: Optional[float],
    notion_interaction_id: Optional[str] = None,
) -> None:
    Agent().execute(query, task, budget, notion_interaction_id)
