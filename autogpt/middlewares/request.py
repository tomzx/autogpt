from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from autogpt.middlewares.response import Response


class Request:
    task: str
    prompt: str
    # TODO(tom@tomrochette.com): Find a way to move this out of this class
    notion_session_id: Optional[str]
    notion_interaction_id: Optional[str]
    needs: List[Response]

    def __init__(self, prompt: str, task: str) -> None:
        self.prompt = prompt
        self.task = task
        self.notion_session_id = None
        self.notion_interaction_id = None
        self.needs = []
