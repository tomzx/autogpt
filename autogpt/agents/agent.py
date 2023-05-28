import time
from collections import deque
from datetime import datetime
from typing import List, Optional

import structlog
from distributed.threadpoolexecutor import ThreadPoolExecutor
from tortoise import Tortoise

from autogpt.backends.debug.debug import Debug
from autogpt.backends.openai.api import Api
from autogpt.budget.money_budget import MoneyBudget
from autogpt.configuration.configuration import Configuration
from autogpt.memory.ram import RAM
from autogpt.middlewares.call_llm import CallLLM
from autogpt.middlewares.execute import call
from autogpt.middlewares.middleware import Middleware
from autogpt.middlewares.next_requests import NextRequests
from autogpt.middlewares.profiler import Profiler
from autogpt.middlewares.remember_interaction import RememberInteraction
from autogpt.middlewares.request import Request
from autogpt.middlewares.response import Response
from autogpt.middlewares.response_graph import ResponseGraph
from autogpt.middlewares.save_to_notion import SaveToNotion
from autogpt.notion.notion import Notion
from autogpt.notion.notion_task import NotionTask
from autogpt.session.session import Session
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
        self.notion = Notion()
        # asyncio.run(self.initialize_database())

    async def initialize_database(self) -> None:
        # TODO(tom@tomrochette.com): Plan for per agent database
        await Tortoise.init(
            db_url="sqlite://db.sqlite3",
            modules={"models": ["autogpt.models"]},
        )
        await Tortoise.generate_schemas()

    def get_middlewares(self) -> List[Middleware]:
        llm = Debug()
        if not is_debug():
            llm = Api(Configuration.open_api_key)

        middlewares = [
            CallLLM(llm),
            # TODO(tom@tomrochette.com): Add a middleware that would prevent the CallLLM
            # middleware from being called if the task does not need to call the LLM.
            RememberInteraction(RAM(), self.session),
            SaveToNotion(self.notion),
            # SaveToDatabase(self.session.model()),
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
        background: bool = False,
        notion_interaction_id: Optional[str] = None,
    ) -> Response:
        logger.debug(
            "Agent starting",
            request=request,
            task=task,
            budget=budget,
            background=background,
            notion_interaction_id=notion_interaction_id,
        )

        middlewares = self.get_middlewares()

        initial_request = None
        response = None
        while background or initial_request is None:
            notion_task: Optional[NotionTask] = None
            if background:
                logger.debug("Getting task from notion")
                notion_task = self.notion.get_next_executable_task()
                if notion_task is None:
                    logger.debug("No task to process, sleeping for 60 seconds")
                    time.sleep(60)
                    continue
                self.notion.update_task(notion_task, "In progress", datetime.now())
                logger.debug("Starting task", task=notion_task.task_id)
                initial_request = notion_task.request
                budget = notion_task.budget
            else:
                if request is None:
                    raise ValueError("Prompt cannot be empty")
                initial_request = Request(request, task)
                initial_request.notion_interaction_id = notion_interaction_id

            notion_session_id = self.notion.start_session(budget)
            if notion_session_id is not None:
                initial_request.notion_session_id = notion_session_id
                if notion_task is not None:
                    self.notion.update_task(notion_task, session_id=notion_session_id)

            self.session.start()
            self.money_budget.set_budget(budget)

            next_requests = NextRequests()
            next_requests.add(initial_request)
            # TODO(tom@tomrochette.com): Replace with a priority
            requests = deque([next_requests])

            while requests:
                if self.should_terminate():
                    logger.debug("Budget exhausted")
                    break

                request_graph = requests.popleft()

                response = self.execute_one(request_graph, middlewares)

                if len(response.next_requests.nodes) > 0:
                    requests += [response.next_requests]

                # TODO(tom@tomrochette.com): Determine when it can delegate to other agents

            logger.debug("No more requests to process")

            self.session.end()

            if notion_task is not None:
                self.notion.update_task(notion_task, "Done", finished=datetime.now())
                logger.debug("Task completed", task=notion_task.task_id)

        return response

    def execute_one(self, request_graph: NextRequests, middlewares: List[Middleware]) -> Response:
        response_graph = execute_graph(request_graph, middlewares)
        response = response_graph.get_output()
        logger.debug("Response", response=response.response)

        self.money_budget.update_spent_budget(response.cost)

        return response

    def should_terminate(self) -> bool:
        return self.money_budget.is_budget_reached()


def execute(
    query: str,
    task: str,
    budget: Optional[float],
    background: bool = False,
    notion_interaction_id: Optional[str] = None,
) -> None:
    Agent().execute(query, task, budget, background, notion_interaction_id)


def execute_graph(request_graph: NextRequests, middlewares):
    futures = {}
    with ThreadPoolExecutor(max_workers=100) as executor:
        for node in request_graph.nodes:
            needs_futures = [futures[need] for need in node.needs]
            futures[node] = executor.submit(call_middleware, middlewares, node.request, needs_futures)

    return ResponseGraph([future.result() for future in futures.values()])


def call_middleware(middlewares, request: Request, needs) -> Response:
    if needs:
        request.needs = [future.result() for future in needs]
    return call(middlewares, request)
