import asyncio
import os
import time
from collections import deque
from typing import List, Optional

import structlog
from dask import compute, delayed
from distributed.threadpoolexecutor import ThreadPoolExecutor
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
from autogpt.middlewares.response import Response
from autogpt.middlewares.response_graph import ResponseGraph
from autogpt.middlewares.save_to_database import SaveToDatabase
from autogpt.middlewares.save_to_notion import SaveToNotion
from autogpt.notion.notion import Notion
from autogpt.session.session import Session
from autogpt.tasks.next_requests import NextRequests
from autogpt.utils.debug import is_debug, is_profiling

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
        llm = Debug()
        if not is_debug():
            llm = Api(os.environ.get("OPENAI_API_KEY"))

        middlewares = [
            CallLLM(llm),
            # TODO(tom@tomrochette.com): Add a middleware that would prevent the CallLLM
            # middleware from being called if the task does not need to call the LLM.
            RememberInteraction(RAM(), self.session),
            SaveToNotion(Notion(), self.money_budget),
            SaveToDatabase(self.session.model()),
        ]

        if is_profiling():
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
        next_requests = NextRequests()
        next_requests.add(initial_request)
        # TODO(tom@tomrochette.com): Replace with a priority
        requests = deque([next_requests])
        while True:
            if not requests:
                logger.debug("No more requests to process")
                break

            if self.should_terminate():
                logger.debug("Budget exhausted")
                break

            request_graph = requests.popleft()

            # Set properties on the request
            request_graph.session = self.session

            response_graph = execute_graph(request_graph, middlewares)
            response = response_graph.get_output()
            logger.debug("Response", response=response.response)

            if len(response.next_requests.nodes) > 0:
                requests += [response.next_requests]

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


def execute_graph(request_graph: NextRequests, middlewares):
    futures = {}
    with ThreadPoolExecutor() as executor:
        for node in request_graph.nodes:
            needs_futures = [futures[need] for need in node.needs]
            futures[node] = executor.submit(call_middleware, middlewares, node.request, needs_futures)

    return ResponseGraph([future.result() for future in futures.values()])


def call_middleware(middlewares, request: Request, needs) -> Response:
    if needs:
        request.needs = [future.result() for future in needs]
    return call(middlewares, request)
