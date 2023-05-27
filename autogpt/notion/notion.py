import os
from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from notion_client import Client

from autogpt.middlewares.request import Request
from autogpt.notion.notion_task import NotionTask

logger = structlog.get_logger(__name__)


class Notion:
    def __init__(self):
        self.client = Client(auth=os.environ.get("NOTION_TOKEN"))

    def has_api_token(self) -> bool:
        return os.environ.get("NOTION_TOKEN") is not None

    def create_session(self, budget: float) -> Dict[str, Any]:
        return self.client.pages.create(
            parent={"database_id": os.environ.get("NOTION_SESSION_DATABASE_ID")},
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
            parent={"database_id": os.environ.get("NOTION_INTERACTION_DATABASE_ID")},
            properties=properties,
        )

    def find_next_executable_task(self) -> Dict[str, Any]:
        return self.client.databases.query(
            database_id=os.environ.get("NOTION_TASK_DATABASE_ID"),
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
        self, task: NotionTask, status: Optional[str], started: datetime = None, finished: Optional[datetime] = None
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

        logger.debug("Updating task", task_id=task.task_id, status=status, started=started, finished=finished)
        return self.client.pages.update(page_id=task.task_id, properties=properties)
