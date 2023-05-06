import os
from datetime import datetime
from typing import Any, Dict

from notion_client import Client


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
                                "content": datetime.now().isoformat(
                                    timespec="milliseconds"
                                ),
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
        self, prompt: str, response: str, session: str, parent: str, cost: float,
    ) -> Dict[str, Any]:
        properties = {
            "Prompt": {
                "title": [
                    {
                        "text": {
                            "content": prompt,
                        },
                    },
                ],
            },
            "Response": {
                "rich_text": [
                    {
                        "text": {
                            "content": response,
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
