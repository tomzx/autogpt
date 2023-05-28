from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from notion_client import Client

from autogpt.configuration.configuration import Configuration
from autogpt.middlewares.request import Request
from autogpt.notion.notion_task import NotionTask
from autogpt.utils.debug import is_debug

logger = structlog.get_logger(__name__)


class Notion:
    def __init__(self):
        self.client = Client(auth=Configuration.notion_token)

    def has_api_token(self) -> bool:
        return Configuration.notion_token is not None

    def create_session(self, budget: float) -> Dict[str, Any]:
        return self.client.pages.create(
            parent={"database_id": Configuration.notion_session_database_id},
            properties={
                "Id": {
                    "title": [
                        {
                            "text": {
                                "content": datetime.now().isoformat(timespec="milliseconds"),
                            },
                        },
                    ],
                },
                "Budget": {
                    "number": budget,
                },
            },
        )

    def start_session(self, budget: float) -> Optional[str]:
        if is_debug() or not self.has_api_token():
            return None

        session = self.create_session(budget)
        logger.debug("Notion session started", session_id=session["id"])
        return session["id"]

    def create_interaction(
        self,
        prompt: str,
        response: str,
        task: str,
        session: str,
        parent: str,
        cost: float,
    ) -> Dict[str, Any]:
        # TODO(tom@tomrochette.com): Handle prompts that are longer than 2000 characters
        # by putting the text in a separate field
        properties = {
            "Prompt": {
                "title": [
                    {
                        "text": {
                            "content": prompt[:2000],
                        },
                    },
                ],
            },
            "Response": {
                "rich_text": [
                    {
                        "text": {
                            "content": response[:2000],
                        },
                    },
                ],
            },
            "Task": {
                "rich_text": [
                    {
                        "text": {
                            "content": task,
                        },
                    },
                ],
            },
            "Cost": {
                "number": cost,
            },
            "Session": {
                "relation": [
                    {
                        "id": session,
                    },
                ],
            },
            "Parent": {
                "relation": [
                    {
                        "id": parent,
                    },
                ],
            },
        }

        if parent is None:
            del properties["Parent"]

        return self.client.pages.create(
            parent={"database_id": Configuration.notion_interaction_database_id},
            properties=properties,
        )

    def find_next_executable_task(self) -> Dict[str, Any]:
        return self.client.databases.query(
            database_id=Configuration.notion_task_database_id,
            filter={
                "and": [
                    {
                        "property": "Status",
                        "status": {
                            "equals": "Not started",
                        },
                    },
                    {
                        "property": "Budget",
                        "number": {
                            "greater_than": 0,
                        },
                    },
                ],
            },
            sorts=[
                {
                    "property": "Created",
                    "direction": "ascending",
                }
            ],
            page_size=1,
        )

    def get_next_executable_task(self) -> Optional[NotionTask]:
        results = self.find_next_executable_task()
        if len(results["results"]) != 1:
            return None

        properties = results["results"][0]["properties"]
        request = properties["Query"]["title"][0]["plain_text"]
        task = properties["Task"]["select"]["name"]
        budget = properties["Budget"]["number"]
        task_id = results["results"][0]["id"]
        return NotionTask(Request(request, task), budget, task_id)

    def update_task(
        self,
        task: NotionTask,
        status: Optional[str] = None,
        started: datetime = None,
        finished: Optional[datetime] = None,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        properties = {}
        if status is not None:
            properties["Status"] = {
                "status": {
                    "name": status,
                },
            }
        if started is not None:
            properties["Started"] = {
                "date": {
                    "start": started.isoformat(),
                },
            }
        if finished is not None:
            properties["Finished"] = {
                "date": {
                    "start": finished.isoformat(),
                },
            }
        if session_id is not None:
            properties["Session"] = {
                "relation": [
                    {
                        "id": session_id,
                    },
                ],
            }

        logger.debug(
            "Updating task",
            task_id=task.task_id,
            status=status,
            started=started.isoformat() if started is not None else None,
            finished=finished.isoformat() if finished is not None else None,
            session_id=session_id,
        )
        return self.client.pages.update(page_id=task.task_id, properties=properties)
